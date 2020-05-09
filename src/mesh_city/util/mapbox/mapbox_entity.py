import math
from pathlib import Path
import requests

class mapbox_entity:
	temp_path = Path(__file__).parents[2]
	images_folder_path = Path.joinpath(temp_path, 'resources','images')

	def __init__(self, google_api_util):
		self.google_api_util = google_api_util
		self.request_number = 0
		self.geocoder = Geocoder(access_token=google_api_util.get_api_key())

	def get_and_store_location(self, x, y, name):
		username = "mapbox"
		style_id = "satellite-v9"
		lat = str(x)
		lon = str(y)
		zoom = str(19)
		bearing = str(0)
		pitch = str(2)
		width = str(640)
		height = str(640)
		scale = "@2x"
		attribution = "attribution=false"
		logo = "logo=false"
		access_token = self.google_api_util.get_api_key()

		response = requests.get("https://api.mapbox.com/styles/v1/" + username + "/"
		                        + style_id + "/" + "static/" + lon + "," + lat + ","
		                        + zoom + "," + bearing + "," + pitch + "/" + width + "x"
		                        + height + scale + "?access_token=" + access_token
		                        + "&" + attribution + "&" + logo)

		filename = name
		to_store = Path.joinpath(self.images_folder_path, filename)

		with open(to_store, 'wb') as output:
			_ = output.write(response.content)

		self.google_api_util.increase_usage()
		#self.increase_request_number()

	def get_location_from_name(self, name):
		#Format to use {house number} {street} {postcode} {city} {state}
		#No semicolons, URL-encoded UTF-8 string, at most 20 words, at most 256 characters
		response = self.geocoder.forward(name)

		if(response.status_code != 200):
				print("No adress could be found")

		collection = response.json()
		most_relevant_response = collection['features'][0]
		coordinates = most_relevant_response['center']
		#coordinates is a list with x and y in reverse order
		return coordinates

	def get_name_from_location(self, x, y):
		response = self.geocoder.reverse(y, x)

		if(response.status_code != 200):
				print("No adress could be found")

		collection = response.json()
		most_relevant_response = collection['features'][0]
		address = most_relevant_response['place_name']
		return address

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
		down = self.calc_next_location_latitude(x,y,20,640,False)
		up = self.calc_next_location_latitude(x,y,20,640,True)
		right = self.calc_next_location_longitude(x,y,20,640,True)
		left = self.calc_next_location_longitude(x,y,20,640,False)

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
