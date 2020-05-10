import math
from pathlib import Path

import geopy.distance
import googlemaps


class GoogleMapsEntity:
	temp_path = Path(__file__).parents[2]
	images_folder_path = Path.joinpath(temp_path, 'resources', 'images')

	def __init__(self, google_api_util):
		self.google_api_util = google_api_util
		self.request_number = 0
		self.client = googlemaps.Client(key=self.google_api_util.get_api_key())

	def get_and_store_location(self, x_coord, y_coord):
		size = (640, 640)
		center = (x_coord, y_coord)
		zoom = 20
		scale = 2
		file_format = "png"
		map_type = "satellite"
		language = None
		region = None
		markers = None
		path = None
		visible = None
		style = None

		filename = str(self.request_number) + "_" + str(x_coord) + "_" + str(y_coord) + ".png"
		to_store = Path.joinpath(self.images_folder_path, filename)

		with open(to_store, 'wb') as file:
			for chunk in googlemaps.maps.static_map(
				self.client,
				size,
				center,
				zoom,
				scale,
				file_format,
				map_type,
				language,
				region,
				markers,
				path,
				visible,
				style,
			):
				if chunk:
					file.write(chunk)

		self.google_api_util.increase_usage()
		self.increase_request_number()

	def calc_next_location_latitude(self, latitude, longitude, zoom, image_size_x):
		metersPerPx = self.calc_meters_per_px(latitude, zoom)
		next_center_distance_meters = metersPerPx * image_size_x
		new_latitude = latitude + (next_center_distance_meters / 6378137) * (
			180 / math.pi)
		return new_latitude

	def calc_next_location_longitude(self, latitude, longitude, zoom, image_size_y):
		metersPerPx = self.calc_meters_per_px(latitude, zoom)
		next_center_distance_meters = metersPerPx * image_size_y
		new_longitude = longitude + (next_center_distance_meters / 6378137) * (
			180 / math.pi) / math.cos(latitude * math.pi / 180)
		return new_longitude

	def calc_meters_per_px(self, latitude, zoom):
		return 156543.03392 * math.cos(latitude * math.pi / 180) / math.pow(2, zoom)

	def increase_request_number(self):
		old_usage = self.request_number
		self.request_number = old_usage + 1

	# box defined by bottom left and top right coordinate!!!
	def get_area(self, bottom_latitude, left_longitude, top_latitude, right_longitude, zoom, image_size):

		horizontal_width = geopy.distance.distance((bottom_latitude, left_longitude), (bottom_latitude, right_longitude)).m
		vertical_length = geopy.distance.distance((bottom_latitude, left_longitude), (top_latitude, left_longitude)).m

		print("horizontal_width in meters = ", horizontal_width, "\nvertical_length in meters = ", vertical_length)
		print("meters per pixel = ", self.calc_meters_per_px(top_latitude, zoom))

		# TODO do we need a different calculation for vertical? Bottom latitude is biggest: safe call
		total_horizontal_pixels = horizontal_width / self.calc_meters_per_px(top_latitude, zoom)
		total_vertical_pixels = vertical_length / self.calc_meters_per_px(top_latitude, zoom)

		print("total_horizontal_pixels = ", total_horizontal_pixels, "\ntotal_vertical_pixels = ", total_vertical_pixels)

		num_of_images_horizontal = int(math.ceil(total_horizontal_pixels / image_size))
		num_of_images_vertical = int(math.ceil(total_vertical_pixels / image_size))

		print("num_of_images_horizontal = ", num_of_images_horizontal, "\nnum_of_images_vertical = ", num_of_images_vertical)

		latitude_first_image = self.calc_next_location_latitude(bottom_latitude, left_longitude, zoom, image_size / 2)
			# bottom_latitude + ((top_latitude - bottom_latitude) / (num_of_images_vertical * 2))
		longitude_first_image = self.calc_next_location_longitude(bottom_latitude, left_longitude, zoom, image_size / 2)
			# left_longitude + ((left_longitude - right_longitude) / (num_of_images_horizontal * 2))

		current_latitude = latitude_first_image
		current_longitude = longitude_first_image

		number_of_calls = 0

		for vertical in range(num_of_images_vertical):
			for horizontal in range(num_of_images_horizontal):
				self.get_and_store_location(current_latitude, current_longitude)
				print(current_latitude, ",", current_longitude)

				number_of_calls += 1
				print(number_of_calls)

				current_longitude = self.calc_next_location_longitude(current_latitude, current_longitude, zoom, image_size)

			current_longitude = longitude_first_image
			current_latitude = self.calc_next_location_latitude(current_latitude, current_longitude, zoom, image_size)



