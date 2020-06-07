"""
Module which contains code to interact with the top_down providers, organising the requests to
their APIs such that data for larger geographical areas can be made and the results of these
requests are stored on disk.
"""
import os
from pathlib import Path

from PIL import Image
import numpy as np
from mesh_city.util.geo_location_util import GeoLocationUtil
from mesh_city.util.image_util import ImageUtil


class RequestMaker:
	"""
	A class that is responsible for handling requests to different map providers. Based on
	tile_information of the user it calculates all the locations that need to be downloaded, downloads them
	stores them in tile system: 9 images together make up one tile. These 9 images are, after being downloaded,
	combined into one large image that is displayed on the map.
	:param user_info: information about the user
	:param quota_manager: quota manager associated with the user
	"""

	def __init__(self, user_entity, application, request_manager, top_down_provider=None):
		self.user_entity = user_entity
		self.request_manager = request_manager
		self.top_down_provider = top_down_provider
		self.application = application

		self.file_handler = application.file_handler
		self.log_manager = application.log_manager

		self.image_util = ImageUtil()
		self.geo_location_util = GeoLocationUtil()

		self.request_number = self.log_manager.get_request_number()

		self.temp_list = None
		self.zoom = None
		self.new_folder_path = None

	def compute_3x3_area(self, latitude, longitude, zoom):
		# normalise coordinate input before adding it to coordinate list
		latitude, longitude = self.geo_location_util.normalise_coordinates(
			latitude=latitude, longitude=longitude, zoom=zoom
		)
		bottom = self.geo_location_util.calc_next_location_latitude(
			latitude=latitude, longitude=longitude, zoom=zoom, direction=False
		)
		top = self.geo_location_util.calc_next_location_latitude(
			latitude=latitude, longitude=longitude, zoom=zoom, direction=True
		)
		right = self.geo_location_util.calc_next_location_longitude(
			latitude=latitude, longitude=longitude, zoom=zoom, direction=True
		)
		left = self.geo_location_util.calc_next_location_longitude(
			latitude=latitude, longitude=longitude, zoom=zoom, direction=False
		)
		return bottom, left, top, right

	def check_zoom(self, zoom):
		if zoom is None:
			zoom = self.top_down_provider.max_zoom
		if zoom < 1:
			zoom = 1
		if zoom > self.top_down_provider.max_zoom:
			zoom = self.top_down_provider.max_zoom
		return zoom

	def make_mock_request(self, image_id, latitude, longitude, folder_path, zoom):
		"""
		Not even for real testing, only developing (should be removed!)
		:param image_id:
		:param latitude:
		:param longitude:
		:param folder_path:
		:param zoom:
		:return:
		"""
		if self.request_manager.is_in_grid(latitude, longitude):
			return self.request_manager.get_path_from_grid(latitude, longitude)
		file_name = str(str(image_id) + "_" + str(longitude) + "_" + str(latitude) + ".png")

		result_file_path = str(
			self.faux_get_store(
			latitude=latitude,
			longitude=longitude,
			zoom=zoom,
			file_name=file_name,
			folder_path=folder_path
			)
		)
		return result_file_path

	def faux_get_store(self,latitude,longitude,zoom,file_name,folder_path):
		array = np.zeros([512, 512, 3], dtype=np.uint8)
		array.fill(255)
		image = Image.fromarray(array)
		path = Path(folder_path).joinpath(file_name)
		image.save(path)
		return path

	def make_single_request(self, image_id, latitude, longitude, folder_path, zoom):
		if self.request_manager.is_in_grid(latitude, longitude):
			return self.request_manager.get_path_from_grid(latitude, longitude)
		file_name = str(image_id + "_" + longitude + "_" + latitude + ".png")

		result_file_path = str(
			self.top_down_provider.get_and_store_location(
			latitude=latitude,
			longitude=longitude,
			zoom=zoom,
			filename=file_name,
			new_folder_path=folder_path
			)
		)
		return result_file_path

	def make_location_request(self, latitude, longitude, zoom=None):
		zoom = self.check_zoom(zoom)
		bottom, left, top, right = self.compute_3x3_area(latitude, longitude, zoom)
		return self.make_area_request(bottom, left, top, right, zoom)

	def make_area_request(
		self, bottom_latitude, left_longitude, top_latitude, right_longitude, zoom=None
	):
		zoom = self.check_zoom(zoom=zoom)
		coordinates, width, height = self.calculate_coordinates_for_rectangle(
			bottom_lat=bottom_latitude,
			left_long=left_longitude,
			top_lat=top_latitude,
			right_long=right_longitude,
			zoom=zoom
		)
		paths = []
		current_request = "request_42"
		folder = Path.joinpath(self.file_handler.folder_overview["image_path"],current_request,"google_maps")
		os.makedirs(str(folder))
		for (index, (latitude,longitude)) in enumerate(coordinates):
			paths.append(self.make_mock_request(index,latitude,longitude,folder,zoom))


	def calculate_coordinates_for_location(self, latitude, longitude, zoom=None):
		zoom = self.check_zoom(zoom)
		bottom, left, top, right = self.compute_3x3_area(latitude, longitude, zoom)
		return self.calculate_coordinates_for_rectangle(bottom, left, top, right, zoom)

	def calculate_coordinates_for_rectangle(
		self, bottom_lat, left_long, top_lat, right_long, zoom=None
	):
		zoom = self.check_zoom(zoom)
		(bottom_lat, left_long), (top_lat,
			right_long) = self.geo_location_util.get_bottom_left_top_right_coordinates(
			(bottom_lat, left_long), (top_lat, right_long)
			)
		# normalise coordinate input before adding it to coordinate list
		latitude_first_image, longitude_first_image = self.geo_location_util.normalise_coordinates(
			bottom_lat, left_long, zoom)
		current_latitude, current_longitude = latitude_first_image, longitude_first_image

		coordinates_list = []
		num_of_images_horizontal = 0
		num_of_images_vertical = 0
		# iterate from left to right, bottom to top
		while current_latitude <= top_lat or current_latitude == 0:
			num_of_images_horizontal = 0
			while current_longitude <= right_long or current_longitude == 0:
				coordinates_list.append((current_latitude, current_longitude))
				current_longitude = self.geo_location_util.calc_next_location_longitude(
					current_latitude, current_longitude, zoom, True
				)
				num_of_images_horizontal += 1
			current_longitude = longitude_first_image
			current_latitude = self.geo_location_util.calc_next_location_latitude(
				current_latitude, current_longitude, zoom, True
			)
			num_of_images_vertical += 1
		return coordinates_list, num_of_images_horizontal, num_of_images_vertical

	def count_uncached_tiles(self, coordinates):
		counter = 0
		for (latitude, longitude) in coordinates:
			if not self.request_manager.is_in_grid(latitude, longitude):
				counter += 1
		return counter
