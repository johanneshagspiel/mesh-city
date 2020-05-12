import glob
import math
import os
from pathlib import Path

import geopy
from PIL import Image

from mesh_city.imagery_provider.top_down_provider.ahn_provider import AhnProvider
from mesh_city.imagery_provider.top_down_provider.google_maps_provider import GoogleMapsProvider
from mesh_city.imagery_provider.top_down_provider.mapbox_provider import MapboxProvider


def calc_meters_per_px(latitude, zoom):
	"""
	Method which calculates the number of meters one pixel at this specific latitude and zoom level
	represents.
	:param latitude: respective latitude.
	:param zoom: respective zoom level, accepts a value between 1 and 21. Urban areas have higher
	zoom levels, whilst Antarctica has a zoom level of 16.
	:return: the number of meters one pixel represents in an image.
	"""
	meters_per_px = 156543.03392 * math.cos(latitude * math.pi / 180) / math.pow(2, zoom)
	return meters_per_px


class RequestManager:
	temp_path = Path(__file__).parents[1]
	images_folder_path = Path.joinpath(temp_path, "resources", "images")
	path_to_map_image = Path.joinpath(images_folder_path, "request_0", "tile_0")

	def __init__(self, user_info,quota_manager):
		self.user_info = user_info
		self.quota_manager  =quota_manager
		self.map_entity = GoogleMapsProvider(user_info, quota_manager)

	def make_request(self, coordinates):
		request_number = 1
		request_number_string = str(request_number)

		new_folder_path = Path.joinpath(self.images_folder_path, 'request_' + request_number_string)
		os.makedirs(new_folder_path)

		tile_number = 0
		temp_tile_number = str(tile_number)
		new_folder_path = Path.joinpath(new_folder_path, 'tile_' + temp_tile_number)
		os.makedirs(new_folder_path)
		tile_number += 1

		locations = self.calculate_locations(coordinates)
		number_map_calls = len(locations)

		counter = 1
		lastRound = True

		for location in locations:
			number = str(counter)
			x = str(location[0])
			y = str(location[1])
			temp_name = str(number + "_" + x + "_" + y + ".png")
			self.map_entity.get_and_store_location(
				location[0], location[1], temp_name, new_folder_path
			)
			counter += 1

			if counter == 10 and not lastRound:
				self.concat_images(new_folder_path, counter, tile_number)
				temp_tile_number = str(tile_number)
				new_folder_path = Path.joinpath(new_folder_path, "tile_" + temp_tile_number)
				os.makedirs(new_folder_path)
				counter = 0
				tile_number += 1
			if counter == 10 and lastRound:
				self.concat_images(new_folder_path, request_number, tile_number - 1)
				self.path_to_map_image = new_folder_path


	# box defined by bottom left and top right coordinate
	def get_area(self, bottom_lat, left_long, top_lat, right_long, zoom, image_size):
		"""
		Method which calculates and retrieves the number of images that are necessary have a
		complete imagery set of a certain geographical area. This area is defined by a bounding box.
		The function checks whether the first coordinate inputted is "smaller" than the second
		inputted coordinate.
		:param bottom_lat: the bottom latitude / bottom left coordinate of the bounding box.
		:param left_long: the left longitude / bottom left coordinate of the bounding box.
		:param top_lat: the top latitude / top right coordinate of the bounding box.
		:param right_long: the right longitude / top right coordinate of the bounding box.
		:param zoom: the level of zoom (meters per pixel) the returned images will be.
		:param image_size: the resolution of the images.
		:return: false if the input is an illegal boundary box,
		"""
		if bottom_lat > top_lat or left_long > right_long:
			return False

		horizontal_width = geopy.distance.distance(
			(bottom_lat, left_long), (bottom_lat, right_long)
		).m
		vertical_length = geopy.distance.distance((bottom_lat, left_long), (top_lat, left_long)).m

		# print(
		# 	"horizontal_width in meters = ",
		# 	horizontal_width,
		# 	"\nvertical_length in meters = ",
		# 	vertical_length,
		# 	"\nmeters per pixel = ",
		# 	calc_meters_per_px(top_lat, zoom)
		# )

		# TODO do we need a different calculation for vertical? Bottom latitude is biggest: safe call
		total_horizontal_pixels = horizontal_width / self.calc_meters_per_px(top_lat, zoom)
		total_vertical_pixels = vertical_length / self.calc_meters_per_px(top_lat, zoom)

		# print(
		# 	"total_horizontal_pixels = ",
		# 	total_horizontal_pixels,
		# 	"\ntotal_vertical_pixels = ",
		# 	total_vertical_pixels
		# )

		num_of_images_horizontal = int(math.ceil(total_horizontal_pixels / image_size))
		num_of_images_vertical = int(math.ceil(total_vertical_pixels / image_size))

		# print(
		# 	"num_of_images_horizontal = ",
		# 	num_of_images_horizontal,
		# 	"\nnum_of_images_vertical = ",
		# 	num_of_images_vertical
		# )

		latitude_first_image = self.calc_next_location_latitude(
			bottom_lat, left_long, zoom, image_size / 2, False
		)
		# bottom_latitude + ((top_latitude - bottom_latitude) / (num_of_images_vertical * 2))
		longitude_first_image = self.calc_next_location_longitude(
			bottom_lat, left_long, zoom, image_size / 2, False
		)
		# left_longitude + ((left_longitude - right_longitude) / (num_of_images_horizontal * 2))

		current_latitude = latitude_first_image
		current_longitude = longitude_first_image

		# number_of_calls = 0

		for vertical in range(num_of_images_vertical):
			for horizontal in range(num_of_images_horizontal):
				self.map_entity.get_and_store_location(current_latitude, current_longitude, False)
				print(current_latitude, ",", current_longitude)

				# print(current_latitude, ",", current_longitude)
				# number_of_calls += 1
				# print(number_of_calls)

				current_longitude = self.calc_next_location_longitude(
					current_latitude, current_longitude, zoom, image_size, False
				)

			current_longitude = longitude_first_image
			current_latitude = self.calc_next_location_latitude(
				current_latitude, current_longitude, zoom, image_size, False
			)
		return True

	def calc_next_location_latitude(self, latitude, longitude, zoom, image_size_x, direction):
		meters_per_px = calc_meters_per_px(latitude, zoom)
		next_center_distance_meters = meters_per_px * image_size_x
		if direction:
			new_latitude = latitude + (next_center_distance_meters / 6378137) * (180 / math.pi)
		else:
			new_latitude = latitude - (next_center_distance_meters / 6378137) * (180 / math.pi)
		return new_latitude

	def calc_next_location_longitude(self, latitude, longitude, zoom, image_size_y, direction):
		meters_per_px = calc_meters_per_px(latitude, zoom)
		next_center_distance_meters = meters_per_px * image_size_y
		if direction:
			new_longitude = longitude + (next_center_distance_meters / 6378137) * (180 /
				math.pi) / math.cos(latitude * math.pi / 180)
		else:
			new_longitude = longitude - (next_center_distance_meters / 6378137) * (180 /
				math.pi) / math.cos(latitude * math.pi / 180)
		return new_longitude

	def calculate_locations(self, coordinates):
		longitude = coordinates[0]
		latitude = coordinates[1]
		image_size = 640 - self.map_entity.padding
		down = self.calc_next_location_latitude(longitude, latitude, 20, image_size, False)
		up = self.calc_next_location_latitude(longitude, latitude, 20, image_size, True)
		right = self.calc_next_location_longitude(longitude, latitude, 20, image_size, True)
		left = self.calc_next_location_longitude(longitude, latitude, 20, image_size, False)

		return [
			(up, left),
			(up, latitude),
			(up, right),
			(longitude, left),
			(longitude, latitude),
			(longitude, right),
			(down, left),
			(down, latitude),
			(down, right),
		]  # yapf: disable

	def concat_images(self, new_folder_path, request, tile_number):
		up_left = Image.open(
			glob.glob(Path.joinpath(new_folder_path, "1_*").absolute().as_posix()).pop()
		)
		up_center = Image.open(
			glob.glob(Path.joinpath(new_folder_path, "2_*").absolute().as_posix()).pop()
		)
		up_right = Image.open(
			glob.glob(Path.joinpath(new_folder_path, "3_*").absolute().as_posix()).pop()
		)
		center_left = Image.open(
			glob.glob(Path.joinpath(new_folder_path, "4_*").absolute().as_posix()).pop()
		)
		center_center = Image.open(
			glob.glob(Path.joinpath(new_folder_path, "5_*").absolute().as_posix()).pop()
		)
		center_right = Image.open(
			glob.glob(Path.joinpath(new_folder_path, "6_*").absolute().as_posix()).pop()
		)
		down_left = Image.open(
			glob.glob(Path.joinpath(new_folder_path, "7_*").absolute().as_posix()).pop()
		)
		down_center = Image.open(
			glob.glob(Path.joinpath(new_folder_path, "8_*").absolute().as_posix()).pop()
		)
		down_right = Image.open(
			glob.glob(Path.joinpath(new_folder_path, "9_*").absolute().as_posix()).pop()
		)

		level_0 = self.get_concat_horizontally(
			self.get_concat_horizontally(up_left, up_center), up_right
		)
		level_1 = self.get_concat_horizontally(
			self.get_concat_horizontally(center_left, center_center), center_right
		)
		level_2 = self.get_concat_horizontally(
			self.get_concat_horizontally(down_left, down_center), down_right
		)

		request_string = str(request)
		tile_number_string = str(tile_number)
		temp_name = "request_" + request_string + "_tile_" + tile_number_string
		self.get_concat_vertically(self.get_concat_vertically(level_0, level_1),
			level_2).save(Path.joinpath(new_folder_path, "concat_image_" + temp_name + ".png"))

	def get_concat_horizontally(self, image_1, image_2):
		temp = Image.new("RGB", (image_1.width + image_2.width, image_1.height))
		temp.paste(image_1, (0, 0))
		temp.paste(image_2, (image_1.width, 0))
		return temp

	def get_concat_vertically(self, image_1, image_2):
		temp = Image.new("RGB", (image_1.width, image_1.height + image_2.height))
		temp.paste(image_1, (0, 0))
		temp.paste(image_2, (0, image_1.height))
		return temp
