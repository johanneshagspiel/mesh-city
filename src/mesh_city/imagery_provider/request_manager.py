import math
from pathlib import Path

import geopy
from PIL import Image

from mesh_city.imagery_provider.top_down_provider.ahn_provider import AhnProvider


class RequestManager:
	temp_path = Path(__file__).parents[1]
	images_folder_path = Path.joinpath(temp_path, "resources", "images")

	def __init__(self, user_entity):
		self.user_entity = user_entity
		#self.map_entity = GoogleMapsEntity(user_entity)
		self.map_entity = AhnProvider(user_entity)
		#self.map_entity = MapboxEntity(user_entity)

	def calc_next_location_latitude(self, latitude, longitude, zoom, image_size_x, direction):
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

	def load_images_map(self, x, y):
		image_size = 640 - self.map_entity.padding
		down = self.calc_next_location_latitude(x, y, 20, image_size, False)
		up = self.calc_next_location_latitude(x, y, 20, image_size, True)
		right = self.calc_next_location_longitude(x, y, 20, image_size, True)
		left = self.calc_next_location_longitude(x, y, 20, image_size, False)

		up_left = self.map_entity.get_and_store_location(up, left, "up_left.png")
		up_center = self.map_entity.get_and_store_location(up, y, "up_center.png")
		up_right = self.map_entity.get_and_store_location(up, right, "up_right.png")
		center_left = self.map_entity.get_and_store_location(x, left, "center_left.png")
		center_center = self.map_entity.get_and_store_location(x, y, "center_center.png")
		center_right = self.map_entity.get_and_store_location(x, right, "center_right.png")
		down_left = self.map_entity.get_and_store_location(down, left, "down_left.png")
		down_center = self.map_entity.get_and_store_location(down, y, "down_center.png")
		down_right = self.map_entity.get_and_store_location(down, right, "down_right.png")

		self.concat_images()

	# box defined by bottom left and top right coordinate
	def get_area(self, bottom_lat, left_long, top_lat, right_long, zoom, image_size):
		horizontal_width = geopy.distance.distance(
			(bottom_lat, left_long), (bottom_lat, right_long)
		).m
		vertical_length = geopy.distance.distance((bottom_lat, left_long), (top_lat, left_long)).m

		print(
			"horizontal_width in meters = ",
			horizontal_width,
			"\nvertical_length in meters = ",
			vertical_length
		)
		print("meters per pixel = ", self.calc_meters_per_px(top_lat, zoom))

		# TODO do we need a different calculation for vertical? Bottom latitude is biggest: safe call
		total_horizontal_pixels = horizontal_width / self.calc_meters_per_px(top_lat, zoom)
		total_vertical_pixels = vertical_length / self.calc_meters_per_px(top_lat, zoom)

		print(
			"total_horizontal_pixels = ",
			total_horizontal_pixels,
			"\ntotal_vertical_pixels = ",
			total_vertical_pixels
		)

		num_of_images_horizontal = int(math.ceil(total_horizontal_pixels / image_size))
		num_of_images_vertical = int(math.ceil(total_vertical_pixels / image_size))

		print(
			"num_of_images_horizontal = ",
			num_of_images_horizontal,
			"\nnum_of_images_vertical = ",
			num_of_images_vertical
		)

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

		number_of_calls = 0

		for vertical in range(num_of_images_vertical):
			for horizontal in range(num_of_images_horizontal):
				self.map_entity.get_and_store_location(current_latitude, current_longitude, False)
				print(current_latitude, ",", current_longitude)

				number_of_calls += 1
				print(number_of_calls)

				current_longitude = self.calc_next_location_longitude(
					current_latitude, current_longitude, zoom, image_size, False
				)

			current_longitude = longitude_first_image
			current_latitude = self.calc_next_location_latitude(
				current_latitude, current_longitude, zoom, image_size, False
			)

	def concat_images(self):
		up_left = Image.open(Path.joinpath(self.images_folder_path, "up_left.png"))
		up_center = Image.open(Path.joinpath(self.images_folder_path, "up_center.png"))
		up_right = Image.open(Path.joinpath(self.images_folder_path, "up_right.png"))
		center_left = Image.open(Path.joinpath(self.images_folder_path, "center_left.png"))
		center_center = Image.open(Path.joinpath(self.images_folder_path, "center_center.png"))
		center_right = Image.open(Path.joinpath(self.images_folder_path, "center_right.png"))
		down_left = Image.open(Path.joinpath(self.images_folder_path, "down_left.png"))
		down_center = Image.open(Path.joinpath(self.images_folder_path, "down_center.png"))
		down_right = Image.open(Path.joinpath(self.images_folder_path, "down_right.png"))

		level_0 = self.get_concat_horizontally(
			self.get_concat_horizontally(up_left, up_center), up_right
		)
		level_1 = self.get_concat_horizontally(
			self.get_concat_horizontally(center_left, center_center), center_right
		)
		level_2 = self.get_concat_horizontally(
			self.get_concat_horizontally(down_left, down_center), down_right
		)

		self.get_concat_vertically(self.get_concat_vertically(level_0, level_1),
			level_2).save(Path.joinpath(self.images_folder_path, "large_image.png"))

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
