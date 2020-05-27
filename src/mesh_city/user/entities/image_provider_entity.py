"""
This module contains the image provider log
"""
import json
from calendar import monthrange
from datetime import datetime

from mesh_city.imagery_provider.top_down_provider.ahn_provider import AhnProvider
from mesh_city.imagery_provider.top_down_provider.google_maps_provider import GoogleMapsProvider
from mesh_city.imagery_provider.top_down_provider.mapbox_provider import MapboxProvider
from mesh_city.logs.log_entities.log_entity import LogEntity


class ImageProviderEntity(LogEntity):
	"""
	The image provider log class that stores all information regarding one image provider associated
	with a user such as api key, usage, quota etc.
	"""

	def __init__(
		self, file_handler, json_data=None, type_map_provider=None, api_key=None, quota=None
	):
		"""
		Sets up a image provider, either from json or when created for the first time
		:param file_handler: the file handler needed to store the image provider
		:param json_data: the json from which to load the image provider
		:param type_map_provider: what kind of image provider this is
		:param api_key: the api key associated with the image provider
		:param quota: the quota to be observed
		"""
		super().__init__(path_to_store=file_handler.folder_overview['users.json'][0])
		if (type_map_provider and api_key and quota is not None):
			self.type = type_map_provider
			self.api_key = api_key
			self.usage = {"static_map": 0, "geocoding": 0, "total": 0}
			self.quota = int(quota)
			self.date_reset = self.calculate_end_this_month()
			self.map_entity = self.load_map_entity()
		else:
			self.type = None
			self.api_key = None
			self.usage = None
			self.quota = None
			self.date_reset = None
			self.map_entity = None
			self.load_json(json_data)
			self.map_entity = self.load_map_entity()

	def load_json(self, json_data):
		"""
		Sets the fields of the class based on a json file
		:param json_data:
		:return:
		"""
		self.type = json_data["type"]
		self.api_key = json_data["api_key"]
		self.usage = json_data["usage"]
		self.quota = int(json_data["quota"])
		self.date_reset = json_data["date_reset"]
		self.check_date_reset()

	def for_json(self):
		"""
		Turns the class into a json compliant form
		:return: the class in a json compliant form
		"""
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

	def check_date_reset(self):
		"""
		Checks if the usage should be reset if a new month has started
		:return: nothing (but the usage fields are reset to 0)
		"""
		old_date = datetime.strptime(self.date_reset, "%Y-%m-%d")
		today = datetime.today()

		if (today >= old_date):
			self.usage["static_map"] = 0
			self.usage["geocoding"] = 0
			self.usage["total"] = 0
			self.date_reset = datetime.strftime(self.calculate_end_this_month(), "%Y-%m-%d")

	# pylint: disable=W0613
	def action(self, logs):
		"""
		Action performed when called by the log manager when writing to file
		:param logs: global log context
		:return: just turns the object to json
		"""
		return self.for_json()

	def load_map_entity(self):
		"""
		Loads the approp
		:return:
		"""
		if self.type == "google_maps":
			return GoogleMapsProvider(image_provider_entity=self)
		if self.type == "mapbox":
			return MapboxProvider(image_provider_entity=self)
		if self.type == "ahn":
			return AhnProvider(image_provider_entity=self)
		return None

	def calculate_end_this_month(self):
		"""
		Helper method to calculate the end of a month
		:return: a string containing the end of the month
		"""
		temp_today = datetime.today()
		temp_month = temp_today.month
		temp_year = temp_today.year
		temp_end = monthrange(temp_year, temp_month)
		return str(temp_year) + "-" + str(temp_month) + "-" + str(temp_end[1])
