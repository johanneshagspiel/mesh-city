"""
Module which contains code to interact with the top_down providers, organising the requests to
their APIs such that data for larger geographical areas can be made and the results of these
requests are stored on disk.
"""

import math
import os
from pathlib import Path

from geopy import distance

from mesh_city.imagery_provider.request_creator import RequestCreator
from mesh_city.imagery_provider.top_down_provider.google_maps_provider import GoogleMapsProvider
from mesh_city.util.geo_location_util import GeoLocationUtil
from mesh_city.util.image_util import ImageUtil
from mesh_city.logs.log_entities.building_instructions_request import BuildingInstructionsRequest


class RequestManager:
	"""
	A class that is responsible for handling requests to different map providers. Based on
	tile_information of the user it calculates all the locations that need to be downloaded, downloads them
	stores them in tile system: 9 images together make up one tile. These 9 images are, after being downloaded,
	combined into one large image that is displayed on the map.
	:param user_info: information about the user
	:param quota_manager: quota manager associated with the user
	"""

	def __init__(self, user_entity, application, top_down_provider=None):
		self.user_entity = user_entity
		self.top_down_provider = top_down_provider
		self.application = application

		self.file_handler = application.file_handler
		self.log_manager = application.log_manager

		self.image_util = ImageUtil()
		self.geo_location_util = GeoLocationUtil()

		self.request_number = self.log_manager.get_request_number()

		self.normal_building_instructions = None
		self.temp_list = None

	def make_request_for_block(self, coordinates, zoom=None):
		"""
		Make a request in such a way, that the images are stored in the tile system, are logged in
		the log manager and they can be displayed on the map
		:param centre_coordinates: the location where the image should be downloaded
		:param zoom: the zoom level at which the image should be downloaded
		:return: nothing
		"""
		max_tile_right = 0

		self.normal_building_instructions = {}
		self.normal_building_instructions["Paths"] = []
		self.normal_building_instructions["Coordinates"] = []

		if len(coordinates) == 9:
			self.normal_building_instructions["Paths"].append(0)
			self.normal_building_instructions["Coordinates"].append(0)

		if len(coordinates) > 9:
			temp = coordinates.pop(0)
			max_latitude = temp[0]
			max_tile_right = int(temp[1])

			self.normal_building_instructions["Paths"].append(int(temp[1]))
			self.normal_building_instructions["Coordinates"].append(int(temp[1]))

		self.zoom = zoom

		if zoom is None:
			self.zoom = self.top_down_provider.max_zoom

		request_number = self.log_manager.get_request_number()
		request_number_string = str(request_number)

		# a new folder is created for the request if it goes ahead
		new_folder_path_request = Path.joinpath(
			self.file_handler.folder_overview["image_path"], "request_" + request_number_string
		)
		os.makedirs(new_folder_path_request)

		# a new folder is created to store all the images in
		self.new_folder_path = Path.joinpath(new_folder_path_request, "google_maps")
		os.makedirs(self.new_folder_path)

		# some information to show in the terminal
		number_tile_downloaded = 0
		tile_number_latitude = 0
		tile_number_longitude = 0

		#bounding_box = [tile_information[0], tile_information[-1]]

		number_requests = len(coordinates)
		print("Requestnumber: " + str(self.request_number))
		print("Total Images to download: " + str(number_requests))

		number_requests_temp = number_requests
		total_tile_numbers = number_requests / 9

		overall_list_coordinates = []
		temp_list_coordinates = []

		overall_list_path = []
		temp_list_path = []

		to_download = []
		to_download_positions = []

		round_counter = 0
		position_counter = 1

		for location in coordinates:
			if position_counter == 10:
				overall_list_coordinates.append(temp_list_coordinates)
				temp_list_coordinates = []

				overall_list_path.append(temp_list_path)
				temp_list_path = []

				position_counter = 1
				round_counter += 1

			if location[1] is None:
				temp_list_coordinates.append(location[0])
				to_download.append((location[0], position_counter))
				to_download_positions.append((round_counter, position_counter - 1))
				temp_list_path.append(None)
			else:
				temp_list_coordinates.append(location[0])
				temp_list_path.append(location[1])
			position_counter += 1

		overall_list_coordinates.append(temp_list_coordinates)
		overall_list_path.append(temp_list_path)

		downloaded_images = list(map(lambda x : self.get_missing_images(x), to_download))

		temp_counter = 0
		for (round_counter, position_counter) in to_download_positions:
			overall_list_path[round_counter][position_counter] = downloaded_images[temp_counter]
			temp_counter += 1

		self.file_handler.folder_overview["active_tile_path"] = self.new_folder_path
		self.file_handler.folder_overview["active_image_path"] = self.new_folder_path
		self.file_handler.folder_overview["active_request_path"] = self.new_folder_path.parents[0]

		overall_list_path.insert(0, max_tile_right)
		self.normal_building_instructions["Paths"] = overall_list_path

		overall_list_coordinates.insert(0, max_tile_right)
		self.normal_building_instructions["Coordinates"] = overall_list_coordinates

		temp_path_request = Path.joinpath(self.new_folder_path.parents[0],
		                                  "building_instructions_request_" + str(
			                                  request_number) + ".json")
		temp_building_instructions_request = BuildingInstructionsRequest(temp_path_request)
		temp_building_instructions_request.instructions[
			self.top_down_provider.name] = self.normal_building_instructions
		self.log_manager.create_log(temp_building_instructions_request)

		self.log_manager.write_log(self.file_handler.coordinate_overview)

		temp_request_creator = RequestCreator(application=self.application)

		temp_path = Path.joinpath(self.file_handler.folder_overview["temp_image_path"],
		                          "concat_image_normal.png")
		temp_request_creator.follow_create_instructions([self.top_down_provider.name, "Paths"],
		                                                temp_building_instructions_request, temp_path)
		self.file_handler.change("active_image_path",
		                         self.file_handler.folder_overview["temp_image_path"])

		return self.new_folder_path

	def get_missing_images(self, location):
		number = str(location[1])
		latitude = str(location[0][0])
		longitude = str(location[0][1])
		temp_name = str(number + "_" + longitude + "_" + latitude + ".png")
		temp_location_stored = str(self.top_down_provider.get_and_store_location(
			location[0][0], location[0][1], self.zoom, temp_name, self.new_folder_path
		))

		if latitude in self.file_handler.coordinate_overview.grid:
			new_to_store = self.file_handler.coordinate_overview.grid[latitude]
			new_to_store[longitude] = {self.top_down_provider.name: temp_location_stored}
			self.file_handler.coordinate_overview.grid[latitude] = new_to_store
		else:
			self.file_handler.coordinate_overview.grid[latitude] = {
				longitude: {self.top_down_provider.name: temp_location_stored}}

		return temp_location_stored


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
		tile_information of each image, and its horizontal and vertical position in the grid of images.
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
				"The first coordinate should be beneath and left of the second coordinate"
			)

		side_resolution_image = self.top_down_provider.max_side_resolution_image

		if isinstance(self.top_down_provider, GoogleMapsProvider):
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
		if (num_of_images_horizontal % 3) != 0:
			num_of_images_horizontal += 3 - (num_of_images_horizontal % 3)
		num_of_images_vertical = int(math.ceil(total_vertical_pixels / side_resolution_image))
		if (num_of_images_vertical % 3) != 0:
			num_of_images_vertical += 3 - (num_of_images_vertical % 3)

		num_of_images_total = num_of_images_horizontal * num_of_images_vertical

		latitude_first_image = self.geo_location_util.calc_next_location_latitude(
			bottom_lat, zoom, side_resolution_image / 2, True
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
				current_latitude, zoom, side_resolution_image, True
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
			if (pointer % 3) == 0:
				# if we are two levels up, we are at the top right end of a tile
				if level == 2:
					# in case this is also at the right hand end of the area we are interested in,
					# so now we want to go further up
					if (pointer % max_latitude) == 0:
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
			if counter == max_entry:
				run = False

		return ordered_result

	def calculate_locations(self, coordinates, zoom=None):
		"""
		This method calculates all the locations to be downloaded for one request
		:param coordinates: the central tile_information around which the other image
		:param zoom:
		:return:
		"""
		if zoom is None:
			zoom = self.top_down_provider.max_zoom

		image_size = self.top_down_provider.max_side_resolution_image
		if isinstance(self.top_down_provider, GoogleMapsProvider):
			image_size = 640 - self.top_down_provider.padding

		if len(coordinates) == 2:
			latitude = coordinates[0]
			longitude = coordinates[1]

			bottom = self.geo_location_util.calc_next_location_latitude(
				latitude=latitude, zoom=zoom, image_size_x=image_size, direction=False
			)
			top = self.geo_location_util.calc_next_location_latitude(
				latitude=latitude, zoom=zoom, image_size_x=image_size, direction=True
			)
			right = self.geo_location_util.calc_next_location_longitude(
				latitude=latitude, longitude=longitude, zoom=zoom, image_size_y=image_size, direction=True
			)
			left = self.geo_location_util.calc_next_location_longitude(
				latitude=latitude, longitude=longitude, zoom=zoom, image_size_y=image_size, direction=False
			)

			temp_list = [
				(bottom, left), (bottom, longitude), (bottom, right), (latitude, left),
				(latitude, longitude), (latitude, right), (top, left), (top, longitude), (top, right),
			]  # pylint: disable=invalid-name

			return temp_list

		if len(coordinates) == 4:
			return self.calculate_centre_coordinates_two_coordinate_input_block(
				(coordinates[0], coordinates[1]), (coordinates[2], coordinates[3]), zoom
			)

		raise Exception(
			"Something went wrong with the input, as it doesn't return something "
			"when it should have "
		)

	def check_coordinates(self, coordinates):
		"""
		Method to check whether or not the coordinates are already downloaded
		:param coordinates: the coordinates to check
		:return: a list indicating whether the coordinates are already downloaded or not
		"""
		temp_list = []
		counter=0
		first_round = len(coordinates) > 9

		for location in coordinates:
			if first_round:
				temp_list.append(location)
				first_round = False
			else:
				latitude = str(location[0])
				longitude = str(location[1])

				if latitude in self.file_handler.coordinate_overview.grid:
					if longitude in self.file_handler.coordinate_overview.grid[latitude]:
						temp_list.append(((latitude, longitude), self.file_handler.coordinate_overview.grid[latitude][longitude][self.top_down_provider.name]))
					else:
						temp_list.append(((latitude, longitude), None))
						counter += 1
				else:
					temp_list.append(((latitude, longitude), None))
					counter += 1

		temp_list.insert(0, counter)
		return temp_list
