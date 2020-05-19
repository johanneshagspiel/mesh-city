"""
A top-down provider which can gather information regarding the heights of objects in the Netherlands
"""
import json
import math
import operator
from pathlib import Path

import requests
from PIL import Image
from scipy import spatial

from mesh_city.imagery_provider.top_down_provider.top_down_provider import TopDownProvider
from mesh_city.util.geo_location_util import GeoLocationUtil


class AhnProvider(TopDownProvider):
	"""
	A class which implements the TopDownProvider abstract class. Provides functionality with regards
	to requests about height information of objects in the Netherlands.
	"""
	color_to_height = None # yapf: disable
	temp_path = Path(__file__).parents[2]
	json_folder_path = Path.joinpath(temp_path, 'resources', 'ahn', 'height_to_color.json')

	def __init__(self, user_info, quota_manager):
		"""
		The initialization method
		:param user_info: the user_info class associated with this image provider
		:param quota_manager: the quota manager associated with this image provider
		"""
		TopDownProvider.__init__(self, user_info=user_info, quota_manager=quota_manager)
		self.name = "ahn"
		self.max_zoom = 20
		self.color_to_height = self.load_from_json()
		self.max_side_resolution_image = 640

	def load_from_json(self):
		"""
		Loads the height associated to a color from a json file.
		:return: a dictionary of the type color : height
		"""
		with open(self.json_folder_path, 'r') as json_log:
			data = json_log.read()
		info = json.loads(data)

		new_dictionary = {}

		for key, value in info.items():
			temp_string = ""
			result = []
			end = len(key)
			counter = 0

			for element in key:
				if (element == ","):
					result.append(int(temp_string))
					temp_string = ""
					counter += 1
				if (element == " " or element == "(" or element == ")"):
					counter += 1
				else:
					if (element == ","):
						counter += 1
					else:
						temp_string += element
						counter += 1

						if (counter == end + 1):
							result.append(int(temp_string))

			temp_tuple = (result[0], result[1], result[2])
			new_key = tuple(temp_tuple)
			new_dictionary[new_key] = value

		return new_dictionary

	def store_to_json(self):
		"""
		Stores a new color : height entry in the dictionary and saves that as a json file
		:return: nothing
		"""
		temp = self.color_to_height

		to_store = {}
		for key, value in temp.items():
			to_store[str(key)] = value

		with open(self.json_folder_path, 'w') as json_log:
			json.dump(to_store, fp=json_log)

	def get_and_store_location(self, longitude, latitude, name, new_folder_path):
		"""
		The standard method to get and store one image at a certain location with a certain name.
		Ahn uses
		:param longitude: the longitude of the location of interest in the EPSG:4326 coordinate system
		:param latitude: the latitude of the location of interest in the EPSG:4326 coordinate system
		:param name: the name to store the file under under
		:param new_folder_path: the path where to store the file
		"""

		bounding_box_coordinates = self.calculate_bounding_box(longitude, latitude, 20, 640, 640)

		xmin = str(bounding_box_coordinates[0])
		ymin = str(bounding_box_coordinates[1])
		xmax = str(bounding_box_coordinates[2])
		ymax = str(bounding_box_coordinates[3])
		width = str(640)
		height = str(640)

		response = requests.get(
			"https://geodata.nationaalgeoregister.nl/ahn3/wms?request=GetMap&service=wms&CRS=EPSG:4326&bbox=%s,%s,%s,%s&width=%s&height=%s&layers=ahn3_05m_dsm&styles=ahn3:ahn3_05m_detail&format=image/png&version=1.30"
			% (xmin, ymin, xmax, ymax, width, height)
		)

		filename = name
		to_store = Path.joinpath(new_folder_path, filename)

		with open(to_store, "wb") as output:
			output.write(response.content)

	def calculate_bounding_box(self, latitude, longitude, zoom, image_size_x, image_size_y):
		"""
		Ahn provider does not ask for the central coordinates to get an image but for the bounding
		box encompassing the area
		:param latitude: latitude of the central location one is interested in getting the image from
		:param longitude: longitude of the central location one is interested in getting the image from
		:param zoom: the zoom level of the image one is interested in
		:param image_size_x: the length of the x axis of the image
		:param image_size_y: the length of the y axis of the image
		:return: a list of the coordinates of the bounding box encompassing the area
		"""
		right = GeoLocationUtil.calc_next_location_latitude(latitude, zoom, image_size_x / 2, True)
		left = GeoLocationUtil.calc_next_location_latitude(latitude, zoom, image_size_x / 2, False)
		# 'up' is officially not snake_case naming but does provide the highest readability
		# in this particular case
		up = GeoLocationUtil.calc_next_location_longitude(
			latitude, longitude, zoom, image_size_y / 2, True
		)  # pylint: disable=invalid-name
		down = GeoLocationUtil.calc_next_location_longitude(
			latitude, longitude, zoom, image_size_y / 2, False
		)

		self.check_in_netherlands([(left, down), (right, up)])

		return [left, down, right, up]

	def check_in_netherlands(self, coordinates):
		"""
		Checks for a list of tuples of coordinates whether or not these location fall within the netherlands
		:param coordinates: a list of tuples of coordinates of the from [(latitude_0,longitude_0),..]
		:return:
		"""
		for entry in coordinates:
			if (
				entry[0] < 50.671799068129744 or
				entry[0] > 53.61086457823865 or
				entry[1] < 3.197334098049271 or
				entry[1] > 7.275203841667622
			):  # yapf: disable
				return False
		return True

	def get_height_from_pixel(self, x_location, y_location):
		"""
		Gets the height from an image at the x and y location of the mouse click
		:param x_location: the x location of the pixel
		:param y_location: the y location of the pixel
		:return: the height associated with this pixel
		"""
		temp_path = Path(__file__).parents[2]
		images_folder_path = Path.joinpath(
			temp_path,
			'resources',
			'images',
			'request_5',
			'tile_0',
			'concat_image_request_10_tile_0.png'
		)

		image_temp = Image.open(images_folder_path)
		image = image_temp.load()
		pixels = image[x_location, y_location]

		if pixels in self.color_to_height:
			return self.color_to_height[pixels]

		else:
			temp_keys = self.color_to_height.keys()
			get_cosine_cimilarity = lambda x, y: 1 - spatial.distance.cosine(x, y)
			temp_cosine_list = [get_cosine_cimilarity(x, pixels) for x in temp_keys]

			index, value = max(enumerate(temp_cosine_list), key=operator.itemgetter(1))

			counter = 0
			for value in self.color_to_height.values():
				if (counter == index):
					temp_new_value = value
					break
				counter += 1

			self.color_to_height[pixels] = temp_new_value
			return temp_new_value
