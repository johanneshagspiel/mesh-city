"""
Module which specifies the behaviour for interacting with the mapbox API
"""

from pathlib import Path

import requests
from mapbox import Geocoder

from mesh_city.imagery_provider.top_down_provider.top_down_provider import TopDownProvider


class MapboxProvider(TopDownProvider):
	"""
	MapboxProvider class, an object which contains method to interact with the MapboxProvider API.
	For requesting top-down imagery. Implements the top_down_provider class.
	"""

	def __init__(self, image_provider_entity):
		TopDownProvider.__init__(self, image_provider_entity=image_provider_entity)
		self.geocoder = Geocoder(access_token=image_provider_entity.api_key)
		self.name = "mapbox"
		self.max_zoom = 18
		self.max_side_resolution_image = 640

	def get_and_store_location(
		self,
		latitude,
		longitude,
		zoom,
		filename,
		new_folder_path,
		width=None,
		height=None,
		response=None
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
		:param: response: the response received from google, used in testing.
		:return:
		"""
		if height is None or height > 640:
			height = 640
		if width is None or width > 640:
			width = 640
		username = "mapbox"
		style_id = "satellite-v9"
		lat = str(latitude)
		lon = str(longitude)
		zoom = str(zoom)
		bearing = str(0)
		pitch = str(2)
		width = str(width)
		height = str(height)
		scale = "2x"
		attribution = "attribution=false"
		logo = "logo=false"
		access_token = self.image_provider_entity.api_key
		if response is None:
			response = requests.get(
				"https://api.mapbox.com/styles/v1/%s/%s/static/%s,%s,%s,%s,%s/%sx%s@%s?access_token=%s&%s&%s"
				% (
				username,
				style_id,
				lon,
				lat,
				zoom,
				bearing,
				pitch,
				width,
				height,
				scale,
				access_token,
				attribution,
				logo,
				)
			)

		to_store = Path.joinpath(new_folder_path, filename)

		with open(to_store, "wb") as output:
			output.write(response.content)

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
		# coordinates is a list with x and y in reverse order
		return coordinates

	def get_name_from_location(self, latitude, longitude):
		"""
		Returns a name based on coordinates
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
