"""
Module which specifies the behaviour for interacting with the mapbox API
"""

from pathlib import Path
from typing import Optional

from mapbox import Geocoder
from requests import get, Response

from mesh_city.imagery_provider.top_down_provider.top_down_provider import TopDownProvider


class MapboxProvider(TopDownProvider):
	"""
	MapboxProvider class, an object which contains method to interact with the MapboxProvider API.
	For requesting top-down imagery. Implements the top_down_provider class.
	"""

	def __init__(self, image_provider_entity):
		super().__init__(image_provider_entity=image_provider_entity)
		self.geocoder = Geocoder(access_token=image_provider_entity.api_key)
		self.name = "Mapbox"
		self.max_zoom = 18
		self.max_side_resolution_image = 640

	def get_and_store_location(
		self,
		latitude: float,
		longitude: float,
		zoom: int,
		filename: str,
		new_folder_path: Path,
		width: int = 640,
		height: int = 640,
		response: Optional[Response] = None,
	) -> Path:
		"""
		Method which makes an API call, and saves it in right format. Also removes the Google logo.

		:param latitude: latitude centre coordinate
		:param longitude: latitude centre coordinate
		:param zoom: how zoomed in the image is
		:param filename: name of the to be stored image
		:param new_folder_path: directory for where the file should be saved.
		:param width: the width dimension of the image
		:param height: the height dimension of the image
		:param: response: the response received from google, used in testing.
		:return:
		"""

		assert width <= 640
		assert width > 1
		assert height <= 640
		assert height > 1

		username = "mapbox"
		style_id = "satellite-v9"
		bearing = 0
		pitch = 2
		scale = "2x"
		attribution = "attribution=false"
		logo = "logo=false"
		if response is None:
			response = get(
				"https://api.mapbox.com/styles/v1/%s/%s/static/%f,%f,%d,%d,%d/%dx%d@%s?access_token=%s&%s&%s"
				% (
				username,
				style_id,
				longitude,
				latitude,
				zoom,
				bearing,
				pitch,
				width,
				height,
				scale,
				self.image_provider_entity.api_key,
				attribution,
				logo,
				)
			)

		to_store = new_folder_path.joinpath(filename)

		with open(to_store, "wb") as output:
			output.write(response.content)

		return to_store

	def get_location_from_name(self, name):
		"""
		Returns a geographical location based on a address name.

		:param name:
		:return:
		"""

		# Format to use {house number} {street} {postcode} {city} {state}
		# No semicolons, URL-encoded UTF-8 string, at most 20 words, at most 256 characters
		response = self.geocoder.forward(name)

		if response.status_code != 200:
			print("No adress could be found")

		collection = response.json()
		most_relevant_response = collection["features"][0]
		coordinates = most_relevant_response["center"]
		# tile_information is a list with x_axis and y_axis in reverse order
		return coordinates

	def get_name_from_location(self, latitude, longitude):
		"""
		Returns a name based on tile_information.

		:param latitude:
		:param longitude:
		:return:
		"""

		response = self.geocoder.reverse(longitude, latitude)

		if response.status_code != 200:
			print("No adress could be found")

		collection = response.json()
		most_relevant_response = collection["features"][0]
		address = most_relevant_response["place_name"]
		return address
