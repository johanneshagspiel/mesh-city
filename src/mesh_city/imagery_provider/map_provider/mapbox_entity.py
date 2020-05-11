from pathlib import Path
import requests
from mapbox import Geocoder
from mesh_city.imagery_provider.map_provider.map_entity import MapEntity

class MapboxEntity(MapEntity):

	def __init__(self, user_entity):
		MapEntity.__init__(self, user_entity=user_entity)
		self.geocoder = Geocoder(access_token=user_entity.get_api_key())

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
		access_token = self.user_entity.get_api_key()

		response = requests.get(
			"https://api.mapbox.com/styles/v1/" + username + "/" + style_id + "/" +
			"static/" + lon + "," + lat + "," + zoom + "," + bearing + "," + pitch + "/" +
			width + "x" + height + scale + "?access_token=" + access_token + "&" +
			attribution + "&" + logo
		)

		filename = name
		to_store = Path.joinpath(self.images_folder_path, filename)

		with open(to_store, 'wb') as output:
			output.write(response.content)

		self.user_entity.increase_usage()

	def get_location_from_name(self, name):
		#Format to use {house number} {street} {postcode} {city} {state}
		#No semicolons, URL-encoded UTF-8 string, at most 20 words, at most 256 characters
		response = self.geocoder.forward(name)

		if (response.status_code != 200):
			print("No adress could be found")

		collection = response.json()
		most_relevant_response = collection['features'][0]
		coordinates = most_relevant_response['center']
		#coordinates is a list with x and y in reverse order
		return coordinates

	def get_name_from_location(self, x, y):
		response = self.geocoder.reverse(y, x)

		if (response.status_code != 200):
			print("No adress could be found")

		collection = response.json()
		most_relevant_response = collection['features'][0]
		address = most_relevant_response['place_name']
		return address
