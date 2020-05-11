import googlemaps
import math
from pathlib import Path
from PIL import Image
import requests

import geopy.distance
import googlemaps


class GoogleMapsEntity:
	temp_path = Path(__file__).parents[2]
	images_folder_path = Path.joinpath(temp_path, 'resources','images')

	def __init__(self, google_api_util):
		self.google_api_util = google_api_util
		self.request_number = 0
		self.client = googlemaps.Client(key=self.google_api_util.get_api_key())

	def get_and_store_location(self, x, y, name):
		x = str(x)
		y = str(y)
		zoom = str(20)
		width = str(640)
		height = str(640)
		scale = str(2)
		format = "PNG"
		maptype = "satellite"

		language = None
		region = None
		markers = None
		path = None
		visible = None
		style = None

		response = requests.get("https://maps.googleapis.com/maps/api/staticmap?" +
		                        "center=" + x + "," + y + "&zoom=" + zoom +
		                        "&size=" + width + "x" + height + "&scale=" + scale +
		                        "&format=" + format + "&maptype=" + maptype +
		                        "&key=" + self.google_api_util.get_api_key())

		# filename = str(self.request_number) + "_" + str(x) + "_" + str(y) + ".png"
		filename = name
		to_store = Path.joinpath(self.images_folder_path, filename)

		with open(to_store, 'wb') as output:
			_ = output.write(response.content)

		get_image = Image.open(to_store)
		left = 40
		top = 40
		right = 1240
		bottom = 1240

		filename = name
		to_store = Path.joinpath(self.images_folder_path, filename)

		im1 = get_image.crop(box=(left, top, right, bottom))
		im1.save(fp=to_store)

		self.google_api_util.increase_usage()
		self.increase_request_number()

	def get_location_from_name(self, name):
		result = googlemaps.client.geocode(client=self.client, address=name)
		print(result)

	def get_name_from_location(self, x, y):
		result = googlemaps.client.reverse_geocode(client=self.client,latlng=(x, y))
		print(result)

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

	def load_images_map(self, x, y):
		down = self.calc_next_location_latitude(x,y,20,600,False)
		up = self.calc_next_location_latitude(x,y,20,600,True)
		right = self.calc_next_location_longitude(x,y,20,600,True)
		left = self.calc_next_location_longitude(x,y,20,600,False)

		up_left = self.get_and_store_location(up, left,"up_left.png")
		up_center = self.get_and_store_location(up, y,"up_center.png")
		up_right = self.get_and_store_location(up, right, "up_right.png")
		center_left = self.get_and_store_location(x, left, "center_left.png")
		center_center = self.get_and_store_location(x, y, "center_center.png")
		center_right = self.get_and_store_location(x, right, "center_right.png")
		down_left = self.get_and_store_location(down, left, "down_left.png")
		down_center = self.get_and_store_location(down, y, "down_center.png")
		down_right = self.get_and_store_location(down, right, "down_right.png")

	def increase_request_number(self):
		old_usage = self.request_number
		self.request_number = old_usage + 1

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
				self.get_and_store_location(current_latitude, current_longitude)
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
