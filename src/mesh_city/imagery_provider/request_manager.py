import math
import os
from pathlib import Path
from geopy import distance
from mesh_city.imagery_provider.top_down_provider.mapbox_provider import MapboxProvider
from mesh_city.imagery_provider.top_down_provider.google_maps_provider import GoogleMapsProvider
from mesh_city.util.image_util import ImageUtil
from mesh_city.util.geo_location_util import GeoLocationUtil
from mesh_city.imagery_provider.top_down_provider.ahn_provider import AhnProvider
from mesh_city.imagery_provider.log_manager import LogManager

class RequestManager:
	temp_path = Path(__file__).parents[1]
	images_folder_path = Path.joinpath(temp_path, 'resources', 'images')
	path_to_map_image = Path.joinpath(images_folder_path, 'request_0', 'tile_0')

	def __init__(self, user_info, quota_manager):
		self.user_info = user_info
		self.quota_manager = quota_manager
		self.map_entity = GoogleMapsProvider(user_info=user_info, quota_manager=quota_manager)

		self.log_manager = LogManager()
		self.image_util = ImageUtil()
		self.geo_location_util = GeoLocationUtil()

		self.request_number = self.log_manager.get_request_number()

	def make_single_request(self, centre_coordinates, zoom, height, width):
		self.map_entity.get_and_store_location(
			centre_coordinates[0],
			centre_coordinates[1],
			zoom,
			height,
			width,
			str(centre_coordinates[0]) + ", " + str(centre_coordinates[1]) + ".png",
			self.images_folder_path
		)

	def make_request_for_block(self, centre_coordinates, zoom):
		request_number = self.request_number
		request_number_string = str(request_number)

		new_folder_path = Path.joinpath(self.images_folder_path, 'request_' + request_number_string)
		os.makedirs(new_folder_path)
		self.request_number = 1

		tile_number = 0
		temp_tile_number = str(tile_number)
		new_folder_path = Path.joinpath(new_folder_path, 'tile_' + temp_tile_number)
		os.makedirs(new_folder_path)
		tile_number += 1

		coordinates = self.calculate_locations(centre_coordinates)
		print(len(coordinates))
		bounding_box = [coordinates[0], coordinates[-1]]

		#if(len(centre_coordinates)== 4):
			#bounding_box = [coordinates[0][0], coordinates[-1][-1]
		# if(len(centre_coordinates)== 2):
		# 	bounding_box = [coordinates[0], coordinates[-1]]

		number_requests = len(coordinates)
		number_requests_temp = number_requests
		lastRound = False

		if(number_requests == 9):
			lastRound = True

		counter = 1

		if(len(centre_coordinates) == 4):
			for location in coordinates:
				x = str(location[0])
				y = str(location[1])
				temp_name = str(x + "_" + y + ".png")
				self.map_entity.get_and_store_location(location[0], location[1], zoom, temp_name,
				                                       new_folder_path)
			self.log_manager.write_entry_log(request_number, self.user_info, self.map_entity,
			                                 number_requests, bounding_box, coordinates)

		if (len(centre_coordinates) == 2):
			for location in coordinates:
				number = str(counter)
				x = str(location[0])
				y = str(location[1])
				temp_name = str(number + "_" + x + "_" + y + ".png")
				self.map_entity.get_and_store_location(location[0], location[1], zoom, temp_name,
				                                       new_folder_path)
				counter += 1

				if counter == 10 and lastRound:
					self.image_util.concat_images(new_folder_path, counter, tile_number - 1, "normal")
					self.path_to_map_image = new_folder_path
					self.log_manager.write_entry_log(request_number, self.user_info, self.map_entity,
					                                 number_requests, bounding_box, coordinates)

		# if (len(centre_coordinates) == 4):
		# 	for location in coordinates:
		# 		for element in location:
		# 			number = str(counter)
		# 			x = str(element[0])
		# 			y = str(element[1])
		# 			temp_name = str(number + "_" + x + "_" + y + ".png")
		# 			self.map_entity.get_and_store_location(element[0],
		# 			                                       element[1], self.map_entity.max_zoom, temp_name,
		# 			                                       new_folder_path)
		# 			counter += 1
		#
		# 			if counter == 10 and not lastRound:
		# 				self.image_util.concat_images(new_folder_path, counter, tile_number - 1, "normal")
		# 				temp_tile_number = str(tile_number)
		# 				new_folder_path = Path.joinpath(new_folder_path.parents[0], "tile_" + temp_tile_number)
		# 				os.makedirs(new_folder_path)
		# 				counter = 1
		# 				print(tile_number - 1)
		# 				tile_number += 1
		# 				number_requests_temp = number_requests_temp - 9
		# 				if (number_requests_temp == 9):
		# 					lastRound = True
		#
		# 			if counter == 10 and lastRound:
		# 				self.image_util.concat_images(new_folder_path, counter, tile_number - 1, "normal")
		# 				self.path_to_map_image = new_folder_path
		# 				self.log_manager.write_entry_log(request_number, self.user_info,
		# 				                                 self.map_entity,
		# 				                                 number_requests * 9, bounding_box, coordinates)


	def get_area_coordinates(self, bottom_lat, left_long, top_lat, right_long, zoom):
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
		:return: false if the input is an illegal boundary box,
		"""
		if bottom_lat > top_lat or left_long > right_long:
			raise Exception('The first coordinate should be beneath and left of the second coordinate')

		side_resolution_image = self.map_entity.max_side_resolution_image

		if isinstance(self.map_entity, GoogleMapsProvider):
			# Removes 40 pixels from the sides as that will be necessary to remove the watermarks
			# specific for google maps API
			side_resolution_image = side_resolution_image - 40

		horizontal_width = distance.distance(
			(bottom_lat, left_long), (bottom_lat, right_long)
		).m
		vertical_length = distance.distance((bottom_lat, left_long), (top_lat, left_long)).m

		total_horizontal_pixels = horizontal_width / self.geo_location_util.calc_meters_per_px(top_lat, zoom)
		total_vertical_pixels = vertical_length / self.geo_location_util.calc_meters_per_px(top_lat, zoom)

		num_of_images_horizontal = int(math.ceil(total_horizontal_pixels / side_resolution_image))
		num_of_images_vertical = int(math.ceil(total_vertical_pixels / side_resolution_image))
		num_of_images_total = num_of_images_horizontal * num_of_images_vertical

		latitude_first_image = self.geo_location_util.calc_next_location_latitude(
			bottom_lat, left_long, zoom, side_resolution_image / 2, True
		)
		longitude_first_image = self.geo_location_util.calc_next_location_longitude(
			bottom_lat, left_long, zoom, side_resolution_image / 2, True
		)

		current_latitude = latitude_first_image
		current_longitude = longitude_first_image

		number_of_calls = 0
		

		for vertical in range(num_of_images_vertical):
			for horizontal in range(num_of_images_horizontal):
				self.map_entity.get_and_store_location(current_latitude,
				                                       current_longitude,
				                                       zoom,
				                                       str(current_latitude) + ", " + str(current_longitude) + ".png",
				                                       self.images_folder_path)
				# TODO save the coordinates write seperate method for retrieval
				print(current_latitude, ",", current_longitude)
				number_of_calls += 1
				print(number_of_calls)

				current_longitude = self.geo_location_util.calc_next_location_longitude(
					current_latitude, current_longitude, zoom, side_resolution_image, True
				)

			current_longitude = longitude_first_image
			current_latitude = self.geo_location_util.calc_next_location_latitude(
				current_latitude, current_longitude, zoom, side_resolution_image, True
			)

	def calculate_locations(self, coordinates, multiplier = 1):
		image_size = 640 - self.map_entity.padding

		if(len(coordinates) == 2):
			longitude = coordinates[0]
			latitude = coordinates[1]

			down = self.geo_location_util.calc_next_location_latitude(longitude, latitude, self.map_entity.max_zoom,
			                                        image_size, False, multiplier)
			up = self.geo_location_util.calc_next_location_latitude(longitude, latitude, self.map_entity.max_zoom,
			                                      image_size, True, multiplier)
			right = self.geo_location_util.calc_next_location_longitude(longitude, latitude, self.map_entity.max_zoom,
			                                          image_size, True, multiplier)
			left = self.geo_location_util.calc_next_location_longitude(longitude, latitude, self.map_entity.max_zoom,
			                                         image_size, False, multiplier)

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

		if(len(coordinates) == 4):
			return self.get_area(coordinates[2], coordinates[1], coordinates[0], coordinates[3])
			# start_longitude = coordinates[0]
			# start_latitude = coordinates[1]
			# end_longitude = coordinates[2]
			# end_latitude = coordinates[3]
			#
			# result = []
			# min_latitude_start = start_latitude
			#
			# while start_longitude > end_longitude:
			# 	while start_latitude < end_latitude:
			# 		result.append(self.calculate_locations([start_longitude, start_latitude]))
			# 		start_latitude = self.geo_location_util.calc_next_location_latitude(start_latitude, start_longitude,
			# 		                                                  self.map_entity.max_zoom,
			# 		                                                  image_size, True)
			# 		start_latitude = self.geo_location_util.calc_next_location_latitude(start_latitude, start_longitude,
			# 		                                                  self.map_entity.max_zoom,
			# 		                                                  image_size, True)
			# 		start_latitude = self.geo_location_util.calc_next_location_latitude(start_latitude, start_longitude,
			# 		                                                  self.map_entity.max_zoom,
			# 		                                                  image_size, True)
			#
			# 		if(start_latitude > end_latitude):
			# 			start_latitude = min_latitude_start
			# 			start_longitude = self.geo_location_util.calc_next_location_longitude(start_latitude, start_longitude,
			# 			                                                    self.map_entity.max_zoom,
			# 			                                                    image_size, False)
			# 			start_longitude = self.geo_location_util.calc_next_location_longitude(start_latitude, start_longitude,
			# 			                                                    self.map_entity.max_zoom,
			# 			                                                    image_size, False)
			# 			start_longitude = self.geo_location_util.calc_next_location_longitude(start_latitude, start_longitude,
			# 			                                                    self.map_entity.max_zoom,
			# 			                                                    image_size, False)
			# 			break
			#
			# return result
