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


class AhnProvider(TopDownProvider):
	"""
	A class which implements the TopDownProvider abstract class. Provides functionality with regards
	to requests about height information of objects in the Netherlands.
	"""
	color_to_height = None # yapf: disable
	temp_path = Path(__file__).parents[2]
	json_folder_path = Path.joinpath(temp_path, 'resources', 'ahn', 'height_to_color.json')

	def __init__(self, user_info, quota_manager):
		TopDownProvider.__init__(self, user_info=user_info, quota_manager=quota_manager)
		self.name = "ahn"
		self.max_zoom = 20
		self.color_to_height = self.load_from_json()
		self.max_side_resolution_image = 640

	def load_from_json(self):
		"""

		:return:
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
		right = self.calc_next_location_latitude(latitude, zoom, image_size_x / 2, True)
		left = self.calc_next_location_latitude(latitude, zoom, image_size_x / 2, False)
		# 'up' is officially not snake_case naming but does provide the highest readability
		# in this particular case
		up = self.calc_next_location_longitude(latitude, longitude, zoom, image_size_y / 2, True)  # pylint: disable=invalid-name
		down = self.calc_next_location_longitude(latitude, longitude, zoom, image_size_y / 2, False)

		self.check_in_netherlands(left, down)
		self.check_in_netherlands(right, up)

		return [left, down, right, up]

	def check_in_netherlands(self, latitude, longitude):
		if (
			latitude < 50.671799068129744 or
			latitude > 53.61086457823865 or
			longitude < 3.197334098049271 or
			longitude > 7.275203841667622
		):  # yapf: disable
			print("Height information is only available in the Netherlands - Sorry!")

	def get_height_from_pixel(self, x_location, y_location):

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
			print(self.color_to_height[pixels])
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

	def calc_next_location_latitude(self, latitude, zoom, image_size_x, direction):
		meters_per_px = 156543.03392 * math.cos(latitude * math.pi / 180) / math.pow(2, zoom)
		next_center_distance_meters = meters_per_px * image_size_x
		if direction:
			new_latitude = latitude + (next_center_distance_meters / 6378137) * (180 / math.pi)
		else:
			new_latitude = latitude - (next_center_distance_meters / 6378137) * (180 / math.pi)
		return new_latitude

	def calc_next_location_longitude(self, latitude, longitude, zoom, image_size_y, direction):
		meters_per_px = 156543.03392 * math.cos(latitude * math.pi / 180) / math.pow(2, zoom)
		next_center_distance_meters = meters_per_px * image_size_y
		if direction:
			new_longitude = longitude + (next_center_distance_meters / 6378137) * (180 /
				math.pi) / math.cos(latitude * math.pi / 180)
		else:
			new_longitude = longitude - (next_center_distance_meters / 6378137) * (180 /
				math.pi) / math.cos(latitude * math.pi / 180)
		return new_longitude
