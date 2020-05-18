"""
Module which contains code to interact with the top_down providers, organising the requests to
their API's such that data for larger geographical areas can be made and the results of these
requests are stored on disk.
"""
import csv
import math
import os
from pathlib import Path

from geopy import distance

from mesh_city.imagery_provider.log_manager import LogManager
from mesh_city.imagery_provider.top_down_provider.google_maps_provider import GoogleMapsProvider
from mesh_city.util.geo_location_util import GeoLocationUtil
from mesh_city.util.image_util import ImageUtil


class RequestManager:
	"""
	A class that is responsible for handling requests to different map providers. Based on
	coordinates of the user it calculates all the locations that need to be downloaded, downloads them
	stores them in tile system: 9 images together make up one tile. These 9 images are, after being downloaded,
	combined into one large image that is displayed on the map.
	:param user_info: information about the user
	:param quota_manager: quota manager associated with the user
	"""
	temp_path = Path(__file__).parents[1]
	images_folder_path = Path.joinpath(temp_path, 'resources', 'images')
	path_to_map_image = Path.joinpath(images_folder_path, 'request_0', 'tile_0')

	def __init__(self, user_info, quota_manager, map_entity=None):
		self.user_info = user_info
		self.quota_manager = quota_manager
		if map_entity is None:
			self.map_entity = GoogleMapsProvider(user_info=user_info, quota_manager=quota_manager)
		# self.map_entity = AhnProvider(user_info=user_info, quota_manager=quota_manager)
		# self.map_entity = MapboxProvider(user_info=user_info, quota_manager=quota_manager)

		self.log_manager = LogManager()
		self.image_util = ImageUtil()
		self.geo_location_util = GeoLocationUtil()

		self.request_number = 1

	def make_single_request(self, centre_coordinates, zoom, height, width):
		"""
		Test method to make and store one image. Does not support the tile system and the image can
		not be displayed on the map.
		:param centre_coordinates: the location where the satellite image should be downloaded
		:param zoom: the zoom level at which the image should be downloaded
		:param height: height of the resulting image
		:param width: width of the resulting image
		:return:
		"""
		self.map_entity.get_and_store_location(
			centre_coordinates[0],
			centre_coordinates[1],
			zoom,
			height,
			width,
			str(centre_coordinates[0]) + ", " + str(centre_coordinates[1]) + ".png",
			self.images_folder_path
		)

	def make_request_two_coordinates(self, first_coordinate, second_coordinate, zoom=None):
		"""
		Takes as input two coordinates for a bounding box, a zoom level to specify how zoomed in the
		the images need to be and saves the retrieved images in a semi-structured way on disk.
		:param first_coordinate:
		:param second_coordinate:
		:param zoom:
		:return:
		"""
		if zoom is None:
			zoom = self.map_entity.max_zoom
		if zoom < 1:
			raise Exception("Zoom level  cannot be lower than 1")
		if zoom > self.map_entity.max_zoom:
			zoom = self.map_entity.max_zoom

		coordinates_info = self.calculate_coordinates_two_coordinate_input(
			first_coordinate, second_coordinate, zoom
		)
		coordinates_list = coordinates_info[1]

		self.make_request_list_of_coordinates(coordinates_list, zoom)

	def make_request_list_of_coordinates(self, coordinates_list, zoom, num_of_images_total=None, ):
		"""
		Makes a number of API requests based on the input of a coordinate list.
		:param coordinates_list: list of coordinates, and image positions in the global grid.
		format: (latitude, longitude), (horizontal, vertical)
		horizontal and vertical signal the images position in the world grid
		coordinates_list = coordinates_info[1]
		:param zoom: which level of zoom the imagery should have
		:param num_of_images_total: number of images to be downloaded
		:return: saves all images on disk, and creates an CSV document with metadata.
		"""

		print("Requestnumber: " + str(self.request_number))
		print("Total Images to download: " + str(num_of_images_total))

		new_folder_path = Path.joinpath(
			self.images_folder_path, "request_" + str(self.request_number)
		)
		os.makedirs(new_folder_path)

		# saves metadata to an CSV file
		csv_filename = Path.joinpath(new_folder_path, 'imagery_metadata.csv')
		with open(csv_filename, 'w') as csvfile:
			fieldnames = [
				'image_number', 'horizontal_position', 'vertical_position', 'latitude', 'longitude'
			]
			csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			csv_writer.writeheader()

			image_number = 0
			for info in coordinates_list:
				latitude = info[0][0]
				longitude = info[0][1]
				horizontal_position = info[1][0]
				vertical_position = info[1][1]
				image_number = image_number + 1

				file_name = str(
					str(image_number) + "_" + str(horizontal_position) + "," + str(vertical_position) +
					"_" + str(latitude) + "," + str(longitude) + ".png"
				)
				self.map_entity.get_and_store_location(
					latitude, longitude, zoom, file_name, new_folder_path
				)
				csv_writer.writerow(
					{
					'image_number': str(image_number),
					'horizontal_position': str(horizontal_position),
					'vertical_position': str(vertical_position),
					'latitude': str(latitude),
					'longitude': str(longitude)
					}
				)

	def calculate_number_of_requested_images_two_coordinate_input(
		self, first_coordinate, second_coordinate, zoom
	):
		"""
		Calculates the number of images that will be requested through the API when requesting a
		bounding box with these two coordinates
		:param first_coordinate: of the bounding box.
		:param second_coordinate: of the bounding box.
		:param zoom: the level of zoom (meters per pixel) the returned images will be.
		:return: number of images that will be requested
		"""
		return self.calculate_centre_coordinates_two_coordinate_input(
			first_coordinate, second_coordinate, zoom
		)[0][0]

	def calculate_centre_coordinates_two_coordinate_input(self, first_coordinate, second_coordinate, zoom):
		"""
		Method which calculates and retrieves the number of images that are necessary to have a
		complete imagery set of a certain geographical area. This area is defined by a bounding box.
		:param first_coordinate: of the bounding box.
		:param second_coordinate:  of the bounding box.
		:param zoom: the level of zoom (meters per pixel) the returned images will be.
		:return: a pair which contains as its first value a tuple with the total number of images,
		and the number of images along the axis, and as second value a list of the centre
		coordinates of each image, and its horizontal and vertical position in the grid of images.
		The coordinate list has the following format:
		((current_latitude, current_longitude), (horizontal, vertical))
		The overall returned format is:
		((num_of_images_total, num_of_images_horizontal, num_of_images_vertical), coordinates_list)
		"""

		if first_coordinate[0] < second_coordinate[0]:
			bottom_lat = first_coordinate[0]
			top_lat = second_coordinate[0]
		else:
			bottom_lat = second_coordinate[0]
			top_lat = first_coordinate[0]

		if first_coordinate[1] < second_coordinate[1]:
			left_long = first_coordinate[1]
			right_long = second_coordinate[1]
		else:
			left_long = second_coordinate[1]
			right_long = first_coordinate[1]

		if bottom_lat > top_lat or left_long > right_long:
			raise Exception(
				'The first coordinate should be beneath and left of the second coordinate'
			)

		side_resolution_image = self.map_entity.max_side_resolution_image

		if isinstance(self.map_entity, GoogleMapsProvider):
			# Removes 40 pixels from the sides, as that will be necessary to remove the watermarks
			# specific for google maps API
			side_resolution_image = side_resolution_image - 40

		horizontal_width = distance.distance((bottom_lat, left_long), (bottom_lat, right_long)).m
		vertical_length = distance.distance((bottom_lat, left_long), (top_lat, left_long)).m

		total_horizontal_pixels = horizontal_width / self.geo_location_util.calc_meters_per_px(
			top_lat, zoom
		)
		total_vertical_pixels = vertical_length / self.geo_location_util.calc_meters_per_px(
			top_lat, zoom
		)

		num_of_images_horizontal = int(
			math.floor(1 + total_horizontal_pixels / side_resolution_image)
		)
		num_of_images_vertical = int(math.floor(1 + total_vertical_pixels / side_resolution_image))

		num_of_images_total = num_of_images_horizontal * num_of_images_vertical

		latitude_first_image = self.geo_location_util.calc_next_location_latitude(
			bottom_lat, left_long, zoom, side_resolution_image / 2, True
		)
		longitude_first_image = self.geo_location_util.calc_next_location_longitude(
			bottom_lat, left_long, zoom, side_resolution_image / 2, True
		)

		current_latitude = latitude_first_image
		current_longitude = longitude_first_image

		# number_of_calls = 0
		coordinates_list = list()

		for vertical in range(num_of_images_vertical):
			for horizontal in range(num_of_images_horizontal):
				coordinates_list.append(
					((current_latitude, current_longitude), (horizontal, vertical))
				)
				# print(current_latitude, ",", current_longitude)
				# number_of_calls += 1
				# print(number_of_calls)
				current_longitude = self.geo_location_util.calc_next_location_longitude(
					current_latitude, current_longitude, zoom, side_resolution_image, True
				)
			current_longitude = longitude_first_image
			current_latitude = self.geo_location_util.calc_next_location_latitude(
				current_latitude, current_longitude, zoom, side_resolution_image, True
			)
		return (num_of_images_total, num_of_images_horizontal,
			num_of_images_vertical), coordinates_list

	def make_request_for_block(self, centre_coordinates, zoom=None):
		"""
		Make a request in such a way, that the images are stored in the tile system, are logged in
		the log manager and they can be displayed on the map
		:param centre_coordinates: the location where the image should be downloaded
		:param zoom: the zoom level at which the image should be downloaded
		:return: nothing
		"""

		if zoom is None:
			zoom = self.map_entity.max_zoom
		request_number = self.request_number
		request_number_string = str(request_number)

		new_folder_path = Path.joinpath(self.images_folder_path, "request_" + request_number_string)
		os.makedirs(new_folder_path)

		number_tile_downloaded = 0
		tile_number_latitude = 0
		tile_number_longitude = 0

		temp_tile_number_latitude = str(tile_number_latitude)
		temp_tile_number_longitude = str(tile_number_longitude)
		new_folder_path = Path.joinpath(
			new_folder_path,
			str(number_tile_downloaded) + "_tile_" + temp_tile_number_latitude + "_" +
			temp_tile_number_longitude
		)
		os.makedirs(new_folder_path)

		coordinates = self.calculate_locations(centre_coordinates, zoom)
		bounding_box = [coordinates[0], coordinates[-1]]

		temp = coordinates.pop(0)
		max_latitude = temp[0]
		# max_longitude = temp[1]

		number_requests = len(coordinates)
		print("Requestnumber: " + str(self.request_number))
		print("Total Images to download: " + str(number_requests))
		number_requests_temp = number_requests
		total_tile_numbers = number_requests / 9
		last_round = False

		if number_requests == 9:
			last_round = True

		counter = 1

		if len(centre_coordinates) == 2:
			for location in coordinates:
				number = str(counter)
				x_position = str(location[0])
				y_position = str(location[1])
				temp_name = str(number + "_" + x_position + "_" + y_position + ".png")
				self.map_entity.get_and_store_location(
					location[0], location[1], zoom, temp_name, new_folder_path
				)
				counter += 1

				if counter == 10 and last_round:
					tile_number = str(tile_number_latitude) + "_" + str(tile_number_longitude)
					self.image_util.concat_images(new_folder_path, counter, tile_number, "normal")
					self.path_to_map_image = new_folder_path
					self.log_manager.write_entry_log(
						request_number,
						self.user_info,
						self.map_entity,
						number_requests,
						bounding_box,
						coordinates,
					)

		if len(centre_coordinates) == 4:

			for location in coordinates:
				number = str(counter)
				x_position = str(location[0])
				y_position = str(location[1])
				temp_name = str(number + "_" + x_position + "_" + y_position + ".png")
				self.map_entity.get_and_store_location(
					location[0], location[1], self.map_entity.max_zoom, temp_name, new_folder_path
				)
				counter += 1

				if counter == 10 and not last_round:
					number_tile_downloaded += 1
					tile_number_old = str(tile_number_latitude) + "_" + str(tile_number_longitude)
					self.image_util.concat_images(
						new_folder_path, counter, tile_number_old, "normal"
					)
					tile_number_latitude += 1
					if (tile_number_latitude == max_latitude):
						tile_number_latitude = 0
						tile_number_longitude += 1
					tile_number_new = str(tile_number_latitude) + "_" + str(tile_number_longitude)
					new_folder_path = Path.joinpath(
						new_folder_path.parents[0],
						str(number_tile_downloaded) + "_tile_" + tile_number_new
					)
					print(str(number_tile_downloaded) + "/" + str(total_tile_numbers))
					os.makedirs(new_folder_path)
					counter = 1
					number_requests_temp = number_requests_temp - 9
					if (number_requests_temp == 9):
						last_round = True

				if counter == 10 and last_round:
					number_tile_downloaded += 1
					tile_number = str(tile_number_latitude) + "_" + str(tile_number_longitude)
					self.image_util.concat_images(new_folder_path, counter, tile_number, "normal")
					print(str(number_tile_downloaded) + "/" + str(total_tile_numbers))
					self.path_to_map_image = new_folder_path
					self.log_manager.write_entry_log(
						request_number,
						self.user_info,
						self.map_entity,
						number_requests * 9,
						bounding_box,
						coordinates,
					)

	def calculate_centre_coordinates_two_coordinate_input_block(self, bottom_left, top_right, zoom):
		"""
		CREATES BLOCKS

		Method which calculates and retrieves the number of images that are necessary have a
		complete imagery set of a certain geographical area. This area is defined by a bounding box.
		The function checks whether the first coordinate inputted is "smaller" than the second
		inputted coordinate.
		:param bottom_left: the bottom left coordinate of the bounding box.
		:param top_right: the bottom left coordinate of the bounding box.
		:param zoom: the level of zoom (meters per pixel) the returned images will be.
		:return: a pair which contains as its first value a tuple with the total number of images,
		and the number of images along the axis, and as second value a list of the centre
		coordinates of each image, and its horizontal and vertical position in the grid of images.
		The coordinate list has the following format:
		((current_latitude, current_longitude), (horizontal, vertical))
		The overall returned format is:
		((num_of_images_total, num_of_images_horizontal, num_of_images_vertical), coordinates_list)
		"""

		bottom_lat = bottom_left[0]
		left_long = bottom_left[1]
		top_lat = top_right[0]
		right_long = top_right[1]

		if bottom_lat > top_lat or left_long > right_long:
			raise Exception(
				'The first coordinate should be beneath and left of the second coordinate'
			)

		side_resolution_image = self.map_entity.max_side_resolution_image

		if isinstance(self.map_entity, GoogleMapsProvider):
			# Removes 40 pixels from the sides, as that will be necessary to remove the watermarks
			# specific for google maps API
			side_resolution_image = side_resolution_image - 40

		horizontal_width = distance.distance((bottom_lat, left_long), (bottom_lat, right_long)).m
		vertical_length = distance.distance((bottom_lat, left_long), (top_lat, left_long)).m

		total_horizontal_pixels = horizontal_width / self.geo_location_util.calc_meters_per_px(
			top_lat, zoom
		)
		total_vertical_pixels = vertical_length / self.geo_location_util.calc_meters_per_px(
			top_lat, zoom
		)
		num_of_images_horizontal = int(math.ceil(total_horizontal_pixels / side_resolution_image))

		# to support the tile system, the total number of images to download needs to be divisible by
		# 9 as one tile is 9 images
		if ((num_of_images_horizontal % 9) != 0):
			num_of_images_horizontal += 9 - (num_of_images_horizontal % 9)
		num_of_images_vertical = int(math.ceil(total_vertical_pixels / side_resolution_image))
		if ((num_of_images_vertical % 9) != 0):
			num_of_images_vertical += 9 - (num_of_images_vertical % 9)

		num_of_images_total = num_of_images_horizontal * num_of_images_vertical

		latitude_first_image = self.geo_location_util.calc_next_location_latitude(
			bottom_lat, left_long, zoom, side_resolution_image / 2, True
		)
		longitude_first_image = self.geo_location_util.calc_next_location_longitude(
			bottom_lat, left_long, zoom, side_resolution_image / 2, True
		)

		current_latitude = latitude_first_image
		current_longitude = longitude_first_image

		coordinates_list = list()

		for vertical in range(num_of_images_vertical):
			for horizontal in range(num_of_images_horizontal):
				coordinates_list.append(
					((current_latitude, current_longitude), (horizontal, vertical))
				)

				current_longitude = self.geo_location_util.calc_next_location_longitude(
					current_latitude, current_longitude, zoom, side_resolution_image, True
				)
			current_longitude = longitude_first_image
			current_latitude = self.geo_location_util.calc_next_location_latitude(
				current_latitude, current_longitude, zoom, side_resolution_image, True
			)

		temp_result = (num_of_images_total, num_of_images_horizontal,
			num_of_images_vertical), coordinates_list

		# here, the results need to be rearranged so that the order of coordiantes returned corresponds
		# to one tile after the other. Currently the output is : 0,0 - 1,0 - 2,0 - 3,0 -4,0
		# for the tile system, the output needs to be : 0,0 - 1,0 - 2,0 - 0,1 -1,1 - 1,2 etc.
		result = temp_result[1]
		max_entry = temp_result[0][0]
		max_latitude = temp_result[0][1]
		max_longitude = temp_result[0][1]

		counter = 0
		pointer = 0
		level = 0
		ordered_result = [(max_latitude / 3, max_longitude / 3)]
		run = True

		while run:
			ordered_result.append(result[pointer][0])
			pointer += 1

			# if we moved 3 points to the right, we are at the end of one tile
			if ((pointer % 3) == 0):
				# if we are two levels up, we are at the top right end of a tile
				if (level == 2):
					# in case this is also at the right hand end of the area we are interested in,
					# so now we want to go further up
					if ((pointer % max_latitude) == 0):
						level = 0
					# here we are not at the very right hand of the area we are interested in, so we
					# again have to move down and then to the right
					else:
						pointer -= (2 * max_latitude)
						level -= 2
				# else this means we are on either level zero or one and thus we can go up one more level
				else:
					pointer = pointer - 3 + max_latitude
					level += 1

			counter += 1
			if (counter == max_entry):
				run = False

		return ordered_result

	def calculate_locations(self, coordinates, zoom):
		"""
		This method calculates all the locations to be downloaded for one request
		:param coordinates: the central coordinates around which the other image
		:param zoom:
		:return:
		"""
		image_size = 640 - self.map_entity.padding

		if (len(coordinates) == 2):
			longitude = coordinates[0]
			latitude = coordinates[1]

			down = self.geo_location_util.calc_next_location_latitude(
				longitude, latitude, zoom, image_size, False
			)
			# 'up' is officially not snake_case naming but does provide the highest readability
			# in this particular case
			up = self.geo_location_util.calc_next_location_latitude( # pylint: disable=invalid-name
				longitude, latitude, zoom, image_size, True
			)
			right = self.geo_location_util.calc_next_location_longitude(
				longitude, latitude, zoom, image_size, True
			)
			left = self.geo_location_util.calc_next_location_longitude(
				longitude, latitude, zoom, image_size, False
			)

			return [
				(down, left), (down, latitude), (down, right), (longitude, left),
				(longitude, latitude), (longitude, right), (up, left), (up, latitude), (up, right),
			]  # pylint: disable=invalid-name

		if len(coordinates) == 4:
			return self.calculate_centre_coordinates_two_coordinate_input_block(
				(coordinates[0], coordinates[1]), (coordinates[2], coordinates[3]), zoom
			)

		raise Exception(
			"Something went wrong with the input, as it doesn't return something "
			"when it should have "
		)
