from pathlib import Path

import googlemaps
import requests
from PIL import Image

from mesh_city.imagery_provider.top_down_provider.top_down_provider import TopDownProvider


class GoogleMapsProvider(TopDownProvider):

	def __init__(self, user_info, quota_manager):
		TopDownProvider.__init__(self, user_info=user_info ,quota_manager=quota_manager)
		self.client = googlemaps.Client(key=self.user_info.api_key)
		self.padding = 40
		self.name = "google_maps"

	def get_and_store_location(self, x, y, name, new_folder_path):
		x = str(x)
		y = str(y)
		zoom = str(20)
		width = str(640)
		height = str(640)
		scale = str(2)
		file_format = "PNG"
		map_type = "satellite"
		api_key = self.user_info.api_key

		language = None
		region = None
		markers = None
		path = None
		visible = None
		style = None

		response = requests.get(
			"https://maps.googleapis.com/maps/api/staticmap?center=%s,%s&zoom=%s&size=%sx%s&scale=%s&format=%s&maptype=%s&key=%s"
			% (x, y, zoom, width, height, scale, file_format, map_type, api_key)
		)

		# filename = str(self.request_number) + "_" + str(x) + "_" + str(y) + ".png"
		filename = name
		to_store = Path.joinpath(new_folder_path, filename)

		with open(to_store, "wb") as output:
			output.write(response.content)

		get_image = Image.open(to_store)
		left = 40
		top = 40
		right = 1240
		bottom = 1240

		filename = name
		to_store = Path.joinpath(new_folder_path, filename)

		im1 = get_image.crop(box=(left, top, right, bottom))
		im1.save(fp=to_store)

		self.quota_manager.increase_usage()

	def get_location_from_name(self, name):
		result = googlemaps.client.geocode(client=self.client, address=name)
		print(result)

	def get_name_from_location(self, x, y):
		result = googlemaps.client.reverse_geocode(client=self.client, latlng=(x, y))
		print(result)
