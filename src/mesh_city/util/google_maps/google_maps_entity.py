import googlemaps
import math
from pathlib import Path

class google_maps_entity:
	temp_path = Path(__file__).parents[2]
	images_folder_path = Path.joinpath(temp_path, 'resources','images')

	def __init__(self, google_api_util):
		self.google_api_util = google_api_util
		self.request_number = 0
		self.client = googlemaps.Client(key=self.google_api_util.get_api_key())

	def get_and_store_location(self, x, y, name):
		size = (640, 640)
		center = (x, y)
		zoom = 20
		scale = 2
		format = "png"
		maptype = "satellite"
		language = None
		region = None
		markers = None
		path = None
		visible = None
		style = None

		#filename = str(self.request_number) + "_" + str(x) + "_" + str(y) + ".png"
		filename = name
		to_store = Path.joinpath(self.images_folder_path, filename)

		f = open(to_store, 'wb')
		for chunk in googlemaps.maps.static_map(self.client, size, center, zoom, scale,
		                                        format, maptype, language, region,
		                                        markers, path, visible, style):
			if chunk:
				f.write(chunk)
		f.close()

		self.google_api_util.increase_usage()
		#self.increase_request_number()

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
