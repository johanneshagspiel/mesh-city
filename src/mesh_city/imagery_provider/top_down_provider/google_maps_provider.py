"""
Module which specifies the behaviour for interacting with the static google maps API
"""

from pathlib import Path
from typing import Optional

import googlemaps
from PIL import Image
from requests import get, Response

from mesh_city.imagery_provider.top_down_provider.top_down_provider import TopDownProvider
from mesh_city.util.geo_location_util import GeoLocationUtil

# TODO add documentation explaining the mathematics of this class


class GoogleMapsProvider(TopDownProvider):
	"""
	GoogleMapsProvider class, an object which contains method to interact with the static google
	maps API. For requesting top-down imagery. Implements the top_down_provider class.
	"""

	def __init__(self, image_provider_entity):
		super().__init__(image_provider_entity=image_provider_entity)
		self.client = googlemaps.Client(key=self.image_provider_entity.api_key)
		self.padding = 40
		self.name = "Google Maps"
		self.max_zoom = 20
		self.max_side_resolution_image = 640
		self.geo_location_util = GeoLocationUtil()

	def get_and_store_location(
		self,
		latitude: float,
		longitude: float,
		zoom: int,
		filename: str,
		new_folder_path: Path,
		width: int = 552,
		height: int = 552,
		response: Optional[Response] = None,
	) -> Path:
		"""
		Method which makes an API call, and saves it in right format. Also removes the Google logo.

		:param response: the response received from a request, used in testing
		:param latitude: latitude centre coordinate
		:param longitude: latitude centre coordinate
		:param zoom: how zoomed in the image is
		:param filename: name of the to be stored image
		:param new_folder_path: directory for where the file should be saved.
		:param width: the width dimension of the image
		:param height: the height dimension of the image
		:return:
		"""

		assert width <= 640
		assert width > 1
		assert height <= 640
		assert height > 1

		scale = 2
		file_format = "PNG"
		map_type = "satellite"

		if response is None:
			response = get(
				"https://maps.googleapis.com/maps/api/staticmap?center=%s,%s&zoom=%s&size=%sx%s&scale=%s&format=%s&maptype=%s&key=%s"
				% (
				str(latitude),
				str(longitude),
				str(zoom),
				str(width),
				str(height),
				str(scale),
				file_format,
				map_type,
				self.image_provider_entity.api_key,
				)
			)

		to_store = new_folder_path.joinpath(filename)

		with open(to_store, "wb") as output:
			output.write(response.content)

		get_image = Image.open(to_store)
		left = self.padding
		upper = self.padding
		right = int(width) * 2 - self.padding
		lower = int(height) * 2 - self.padding

		to_store = Path.joinpath(new_folder_path, filename)

		# crop 40 pixels from all sides to remove the watermark
		im1 = get_image.crop(box=(left, upper, right, lower))

		im1.save(fp=to_store)

		return to_store

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
		Returns an address name based on tile_information.

		:param latitude:
		:param longitude:
		:return:
		"""

		result = googlemaps.client.reverse_geocode(client=self.client, latlng=(latitude, longitude))
		print(result)
