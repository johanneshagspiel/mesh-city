import googlemaps.maps
import googlemaps
from pathlib import Path

class google_maps_entity:
	temp_path = Path(__file__).parents[2]
	images_folder_path = Path.joinpath(temp_path, 'resources','images')

	def __init__(self, google_api_util):
		self.google_api_util = google_api_util
		self.request_number = 0
		self.client = googlemaps.Client(key=self.google_api_util.get_api_key())

	def get_and_store_location(self, x, y):

		size = (640, 640)
		center = (x, y)
		zoom = 20
		scale = 1
		format = "PNG"
		maptype = "satellite"
		language = None
		region = None
		markers = None
		path = None
		visible = None
		style = None

		filename = str(self.request_number) + "_" + str(x) + "_" + str(y) + ".png"
		to_store = Path.joinpath(self.images_folder_path, filename)

		f = open(to_store, 'wb')
		for chunk in googlemaps.maps.static_map(self.client, size, center, zoom, scale,
		                                        format, maptype, language, region,
		                                        markers, path, visible, style):
			if chunk:
				f.write(chunk)
		f.close()

		self.google_api_util.increase_usage()
		self.increase_request_number()

	def increase_request_number(self):
		old_usage = self.request_number
		self.request_number = old_usage + 1
