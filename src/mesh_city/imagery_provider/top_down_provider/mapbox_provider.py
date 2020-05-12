from pathlib import Path

import requests
from mapbox import Geocoder

from mesh_city.imagery_provider.top_down_provider.top_down_provider import TopDownProvider


class MapboxProvider(TopDownProvider):

	def __init__(self, user_entity):
		TopDownProvider.__init__(self, user_entity=user_entity)
		self.geocoder = Geocoder(access_token=user_entity.get_api_key())
		self.name = "mapbox"

	def get_and_store_location(self, latitude, longitude, zoom, filename, new_folder_path):
		username = "mapbox"
		style_id = "satellite-v9"
		lat = str(latitude)
		lon = str(longitude)
		zoom = str(zoom)
		bearing = str(0)
		pitch = str(2)
		width = str(640)
		height = str(640)
		scale = "2x"
		attribution = "attribution=false"
		logo = "logo=false"
		access_token = self.user_entity.get_api_key()

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

		self.user_entity.increase_usage()

	def get_location_from_name(self, name):
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

	def get_name_from_location(self, x, y):
		response = self.geocoder.reverse(y, x)

		if response.status_code != 200:
			print("No adress could be found")

		collection = response.json()
		most_relevant_response = collection["features"][0]
		address = most_relevant_response["place_name"]
		return address
