"""
Module which specifies the behaviour for interacting with the static google maps API
"""

from pathlib import Path

import googlemaps
import requests
from PIL import Image

from mesh_city.imagery_provider.top_down_provider.top_down_provider import TopDownProvider


class GoogleMapsProvider(TopDownProvider):
	"""
	GoogleMapsProvider class, an object which contains method to interact with the static google
	maps API. For requesting top-down imagery. Implements the top_down_provider class.
	"""

	def __init__(self, image_provider_entity):
		super().__init__(image_provider_entity=image_provider_entity)
		self.client = googlemaps.Client(key=self.image_provider_entity.api_key)
		self.padding = 40
		self.name = "google_maps"
		self.max_zoom = 20
		self.max_side_resolution_image = 640

	def get_and_store_location(
		self, latitude, longitude, zoom, filename, new_folder_path, width=None, height=None
	):
		"""
		Method which makes an API call, and saves it in right format. Also removes the Google logo.
		:param latitude: latitude centre coordinate
		:param longitude: latitude centre coordinate
		:param zoom: how zoomed in the image is
		:param filename: name of the to be stored image
		:param new_folder_path: directory for where the file should be saved.
		:param width: the width dimension of the image
		:param height: the height dimension of the image
		:return:
		"""

		if height is None or height > 640:
			height = 640
		if width is None or width > 640:
			width = 640
		latitude = str(latitude)
		longitude = str(longitude)
		zoom = str(zoom)
		width = str(width)
		height = str(height)
		scale = str(2)
		file_format = "PNG"
		map_type = "satellite"
		api_key = self.image_provider_entity.api_key

		response = requests.get(
			"https://maps.googleapis.com/maps/api/staticmap?center=%s,%s&zoom=%s&size=%sx%s&scale=%s&format=%s&maptype=%s&key=%s"
			% (latitude, longitude, zoom, width, height, scale, file_format, map_type, api_key)
		)

		to_store = Path.joinpath(new_folder_path, filename)

		with open(to_store, "wb") as output:
			output.write(response.content)

		get_image = Image.open(to_store)
		left = 40
		upper = 40
		right = 1240
		lower = 1240

		to_store = Path.joinpath(new_folder_path, filename)

		# crop 40 pixels from all sides to remove the watermark
		im1 = get_image.crop(box=(left, upper, right, lower))

		im1.save(fp=to_store)

	def get_location_from_name(self, name):
		"""
		Returns a geographical location based on an address name.
		:param name:
		:return:
		"""
		result = googlemaps.client.geocode(client=self.client, address=name)
		print(result)

	def get_name_from_location(self, latitude, longitude):
		"""
		Returns an address name based on coordinates
		:param latitude:
		:param longitude:
		:return:
		"""
		result = googlemaps.client.reverse_geocode(client=self.client, latlng=(latitude, longitude))
		print(result)
