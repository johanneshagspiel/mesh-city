from pathlib import Path
import googlemaps
import requests
from PIL import Image
from mesh_city.imagery_provider.map_provider.map_entity import MapEntity

class GoogleMapsEntity(MapEntity):

	def __init__(self, user_entity):
		MapEntity.__init__(self, user_entity=user_entity)
		self.client = googlemaps.Client(key=self.user_entity.get_api_key())
		self.padding = 40

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

		response = requests.get(
			"https://maps.googleapis.com/maps/api/staticmap?" + "center=" + x + "," + y +
			"&zoom=" + zoom + "&size=" + width + "x" + height + "&scale=" + scale +
			"&format=" + format + "&maptype=" + maptype + "&key=" +
			self.user_entity.get_api_key()
		)

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

		self.user_entity.increase_usage()

	def get_location_from_name(self, name):
		result = googlemaps.client.geocode(client=self.client, address=name)
		print(result)

	def get_name_from_location(self, x, y):
		result = googlemaps.client.reverse_geocode(client=self.client, latlng=(x, y))
		print(result)
