import math
import os
from pathlib import Path
from PIL import Image
import geopy
import glob
from mesh_city.imagery_provider.map_provider.mapbox_entity import MapboxEntity
from mesh_city.imagery_provider.map_provider.google_maps_entity import GoogleMapsEntity
from mesh_city.imagery_provider.map_provider.ahn_entity import AhnEntity


class RequestManager:
	temp_path = Path(__file__).parents[1]
	images_folder_path = Path.joinpath(temp_path, 'resources','images')
	path_to_map_image = None

	def __init__(self, user_entity):
		self.user_entity = user_entity
		self.map_entity = GoogleMapsEntity(user_entity)
		#self.map_entity = AhnEntity(user_entity)
		#self.map_entity = MapboxEntity(user_entity)

	def make_request(self, coordinates):

		request_number = 0
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
				self.map_entity.get_and_store_location(location[0], location[1], temp_name, new_folder_path)
				counter += 1

				if (counter == 10 and lastRound == False):
						self.concat_images(new_folder_path, counter, tile_number)
						temp_tile_number = str(tile_number)
						new_folder_path = Path.joinpath(new_folder_path, 'tile_' + temp_tile_number)
						os.makedirs(new_folder_path)
						counter = 0
						tile_number += 1
				if (counter == 10 and lastRound == True):
						self.concat_images(new_folder_path, request_number, tile_number - 1)
						self.path_to_map_image = new_folder_path

	def calculate_locations(self, coordinates):
		if (len(coordinates) == 2):
			longitude = coordinates[0]
			latitude = coordinates[1]
			image_size = 640 - self.map_entity.padding
			down = self.calc_next_location_latitude(longitude, latitude, 20, image_size, False)
			up = self.calc_next_location_latitude(longitude, latitude, 20, image_size, True)
			right = self.calc_next_location_longitude(longitude, latitude, 20, image_size, True)
			left = self.calc_next_location_longitude(longitude, latitude, 20, image_size, False)

			return [(up, left), (up, latitude), (up, right), (longitude, left),
			        (longitude, latitude), (longitude, right), (down, left), (down, latitude),
			        (down, right)]

	# box defined by bottom left and top right coordinate!!!
	def get_area(
		self,
		bottom_latitude,
		left_longitude,
		top_latitude,
		right_longitude,
		zoom,
		image_size
	):

		horizontal_width = geopy.distance.distance(
			(bottom_latitude, left_longitude), (bottom_latitude, right_longitude)
		).m
		vertical_length = geopy.distance.distance(
			(bottom_latitude, left_longitude), (top_latitude, left_longitude)
		).m

		print(
			"horizontal_width in meters = ",
			horizontal_width,
			"\nvertical_length in meters = ",
			vertical_length
		)
		print("meters per pixel = ", self.calc_meters_per_px(top_latitude, zoom))

		# TODO do we need a different calculation for vertical? Bottom latitude is biggest: safe call
		total_horizontal_pixels = horizontal_width / self.calc_meters_per_px(
			top_latitude, zoom
		)
		total_vertical_pixels = vertical_length / self.calc_meters_per_px(
			top_latitude, zoom
		)

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
			bottom_latitude, left_longitude, zoom, image_size / 2
		)
		# bottom_latitude + ((top_latitude - bottom_latitude) / (num_of_images_vertical * 2))
		longitude_first_image = self.calc_next_location_longitude(
			bottom_latitude, left_longitude, zoom, image_size / 2
		)
		# left_longitude + ((left_longitude - right_longitude) / (num_of_images_horizontal * 2))

		current_latitude = latitude_first_image
		current_longitude = longitude_first_image

		number_of_calls = 0

		for vertical in range(num_of_images_vertical):
			for horizontal in range(num_of_images_horizontal):
				self.map_entity.get_and_store_location(current_latitude, current_longitude)
				print(current_latitude, ",", current_longitude)

				number_of_calls += 1
				print(number_of_calls)

				current_longitude = self.calc_next_location_longitude(
					current_latitude, current_longitude, zoom, image_size
				)

			current_longitude = longitude_first_image
			current_latitude = self.calc_next_location_latitude(
				current_latitude, current_longitude, zoom, image_size
			)

	def calc_next_location_latitude(self, latitude, longitude, zoom, image_size_x, direction):
		metersPerPx = 156543.03392 * math.cos(latitude * math.pi / 180) / math.pow(2, zoom)
		next_center_distance_meters = metersPerPx * image_size_x
		if(direction == True):
			new_latitude = latitude + (next_center_distance_meters / 6378137) * (
				180 / math.pi)
		else:
			new_latitude = latitude - (next_center_distance_meters / 6378137) * (
					180 / math.pi)
		return new_latitude

	def calc_next_location_longitude(self, latitude, longitude, zoom, image_size_y, direction):
		metersPerPx = 156543.03392 * math.cos(latitude * math.pi / 180) / math.pow(2, zoom)
		next_center_distance_meters = metersPerPx * image_size_y
		if (direction == True):
			new_longitude = longitude + (next_center_distance_meters / 6378137) * (
				180 / math.pi) / math.cos(latitude * math.pi / 180)
		else:
			new_longitude = longitude - (next_center_distance_meters / 6378137) * (
				180 / math.pi) / math.cos(latitude * math.pi / 180)
		return new_longitude

	def concat_images(self, new_folder_path, request, tile_number):
		up_left = Image.open(glob.glob(Path.joinpath(new_folder_path, '1_*').absolute().as_posix()).pop())
		up_center = Image.open(glob.glob(Path.joinpath(new_folder_path, '2_*').absolute().as_posix()).pop())
		up_right = Image.open(glob.glob(Path.joinpath(new_folder_path, '3_*').absolute().as_posix()).pop())
		center_left = Image.open(glob.glob(Path.joinpath(new_folder_path, '4_*').absolute().as_posix()).pop())
		center_center = Image.open(glob.glob(Path.joinpath(new_folder_path, '5_*').absolute().as_posix()).pop())
		center_right = Image.open(glob.glob(Path.joinpath(new_folder_path, '6_*').absolute().as_posix()).pop())
		down_left = Image.open(glob.glob(Path.joinpath(new_folder_path, '7_*').absolute().as_posix()).pop())
		down_center = Image.open(glob.glob(Path.joinpath(new_folder_path, '8_*').absolute().as_posix()).pop())
		down_right = Image.open(glob.glob(Path.joinpath(new_folder_path, '9_*').absolute().as_posix()).pop())

		level_0 = self.get_concat_horizontally(self.get_concat_horizontally(
			up_left, up_center), up_right)
		level_1 = self.get_concat_horizontally(self.get_concat_horizontally(
			center_left, center_center), center_right)
		level_2 = self.get_concat_horizontally(self.get_concat_horizontally(
			down_left, down_center), down_right)

		request_string = str(request)
		tile_number_string = str(tile_number)
		temp_name = "request_" + request_string + "_tile_"+ tile_number_string
		self.get_concat_vertically(self.get_concat_vertically(
			level_0, level_1), level_2).save(
			Path.joinpath(new_folder_path, "concat_image_" + temp_name + ".png"))

	def get_concat_horizontally(self, image_1, image_2):
		temp = Image.new('RGB', (image_1.width + image_2.width, image_1.height))
		temp.paste(image_1, (0, 0))
		temp.paste(image_2, (image_1.width, 0))
		return temp


	def get_concat_vertically(self, image_1, image_2):
		temp = Image.new('RGB', (image_1.width, image_1.height + image_2.height))
		temp.paste(image_1, (0, 0))
		temp.paste(image_2, (0, image_1.height))
		return temp
