import googlemaps
import math
from pathlib import Path
from PIL import Image
import requests

class google_maps_entity:
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
		#self.increase_request_number()

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
