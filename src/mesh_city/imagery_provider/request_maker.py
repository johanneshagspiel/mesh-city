"""
Module which contains code to interact with the top_down providers, organising the requests to
their APIs such that data for larger geographical areas can be made and the results of these
requests are stored on disk.
"""
from pathlib import Path

import numpy as np
from PIL import Image

from mesh_city.request.google_layer import GoogleLayer
from mesh_city.request.request import Request
from mesh_city.request.tile import Tile
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

	def make_single_request(self, id, x_cor_current_tile, y_cor_current_tile, folder_path, zoom):
		"""
		Not even for real testing, only developing (should be removed!)
		:param image_id:
		:param latitude:
		:param longitude:
		:param folder_path:
		:param zoom:
		:return:
		"""
		if self.request_manager.is_in_grid(x_cor_current_tile, y_cor_current_tile):
			return self.request_manager.get_tile_from_grid(x_cor_current_tile, y_cor_current_tile)
		file_name = str(str(x_cor_current_tile) + "_" + str(y_cor_current_tile) + ".png")
		latitude,longitude = self.geo_location_util.tile_value_to_degree(
			x_cor_current_tile, y_cor_current_tile, zoom
		)
		result_path = self.top_down_provider.get_and_store_location(
				# id=id,
				latitude=latitude,
				longitude=longitude,
				zoom=zoom,
				filename=file_name,
				new_folder_path=folder_path
			).relative_to(Path.joinpath(self.file_handler.folder_overview["image_path"]))
		return Tile(path=result_path,x_coord=x_cor_current_tile,y_coord=y_cor_current_tile)

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
		tiles = []
		folder = Path.joinpath(self.file_handler.folder_overview["image_path"],
		                       "google_maps")
		folder.mkdir(parents=True, exist_ok=True)
		min_x = None
		min_y = None
		for (index, (x_cor_tile, y_cor_tile)) in enumerate(coordinates):
			if min_x is None:
				min_x=x_cor_tile
				min_y=y_cor_tile
			min_x = min(min_x,x_cor_tile)
			min_y = min(min_y,y_cor_tile)
			request_result = self.make_single_request(index, x_cor_tile, y_cor_tile, folder, zoom)
			tiles.append(request_result)
		request = Request(x_coord=min_x,y_coord=min_y,request_id=self.request_manager.get_new_request_id(), width=width, height=height)
		request.add_layer(GoogleLayer(tiles=tiles))
		return request

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
				x_cor_current_tile, y_cor_current_tile = self.geo_location_util.degree_to_tile_value(
					current_latitude, current_longitude, zoom
				)
				coordinates_list.append((x_cor_current_tile, y_cor_current_tile))
				current_longitude = self.geo_location_util.calc_next_location_longitude(
					current_latitude, current_longitude, zoom, True
				)
				num_of_images_horizontal += 1
			current_longitude = longitude_first_image
			current_latitude = self.geo_location_util.calc_next_location_latitude(
				current_latitude, current_longitude, zoom, True
			)
			num_of_images_vertical += 1
		coordinates_list = sorted(coordinates_list, key=lambda coordinate: coordinate[1])
		return coordinates_list, num_of_images_horizontal, num_of_images_vertical

	def count_uncached_tiles(self, coordinates):
		counter = 0
		for (latitude, longitude) in coordinates:
			if not self.request_manager.is_in_grid(latitude, longitude):
				counter += 1
		return counter
