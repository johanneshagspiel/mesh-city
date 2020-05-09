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

	# TODO remove the magic numbers: this is only defined for zoom level 20
	def calc_next_location_latitude(self, latitude, longitude, zoom, image_size_x):
		meters_per_px = self.calc_meters_per_px(latitude, zoom)
		next_center_distance_meters = meters_per_px * image_size_x
		new_latitude = latitude + (next_center_distance_meters /
			6378137) * (180 / math.pi)
		return new_latitude

	# TODO remove the magic numbers: this is only defined for zoom level 20
	def calc_next_location_longitude(self, latitude, longitude, zoom, image_size_y):
		meters_per_px = self.calc_meters_per_px(latitude, zoom)
		next_center_distance_meters = meters_per_px * image_size_y
		new_longitude = longitude + (next_center_distance_meters /
			6378137) * (180 / math.pi) / math.cos(latitude * math.pi / 180)
		return new_longitude

	def calc_meters_per_px(self, latitude, zoom):
		return 156543.03392 * math.cos(latitude * math.pi / 180) / math.pow(2, zoom)

	def increase_request_number(self):
		old_usage = self.request_number
		self.request_number = old_usage + 1

	# TODO remove magic number 640
	def get_area(
		self,
		left_top_latitude,
		left_top_longitude,
		right_bottom_latitude,
		right_bottom_longitude,
		zoom,
	):
		right_top_latitude = right_bottom_latitude
		right_top_longitude = left_top_longitude
		left_bottom_latitude = left_top_latitude
		left_bottom_longitude = right_bottom_longitude

		horizontal_width = geopy.distance.distance(
			(left_top_latitude, left_top_longitude),
			(right_top_latitude, right_top_longitude),
		).km
		vertical_length = geopy.distance.distance(
			(left_top_latitude, left_top_longitude),
			(left_bottom_latitude, left_bottom_longitude),
		).km

		total_horizontal_pixels = horizontal_width / self.calc_meters_per_px(
			left_top_latitude, zoom
		)
		# TODO do we need a different calculation for vertical?
		total_vertical_pixels = vertical_length / self.calc_meters_per_px(
			right_bottom_latitude, zoom
		)

		num_of_images_horizontal = total_horizontal_pixels / 640
		num_of_images_vertical = total_vertical_pixels / 640

		for vertical in range(num_of_images_vertical):
			for horizontal in range(num_of_images_horizontal):
				pass
