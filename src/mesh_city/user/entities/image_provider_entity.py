"""
This module contains the image provider log
"""
import json
from calendar import monthrange
from datetime import datetime

from mesh_city.imagery_provider.top_down_provider.ahn_provider import AhnProvider
from mesh_city.imagery_provider.top_down_provider.google_maps_provider import GoogleMapsProvider
from mesh_city.imagery_provider.top_down_provider.mapbox_provider import MapboxProvider
from mesh_city.util.logs.log_entry.log_entity import LogEntity


class ImageProviderEntity(LogEntity):
	"""
	The image provider log class
	"""

	def __init__(self, file_handler, json=None, type=None, api_key=None, quota=None):
		self.path_to_store = file_handler.folder_overview['users.json']
		if (type and api_key and quota != None):
			self.type = type
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
			self.load_json(json)
			self.map_entity = self.load_map_entity()

	def load_json(self, json):
		self.type = json["type"]
		self.api_key = json["api_key"]
		self.usage = json["usage"]
		self.quota = int(json["quota"])
		self.date_reset = json["date_reset"]
		self.check_date_reset()

	def for_json(self):
		return json.dumps(self, default=lambda o: o.__dict__,
		                  sort_keys=True, indent=4)

	def check_date_reset(self):
		old_date = datetime.strptime(self.date_reset, "%Y-%m-%d")
		today = datetime.today()

		if (today >= old_date):
			self.usage["static_map"] = 0
			self.usage["geocoding"] = 0
			self.usage["total"] = 0
			self.date_reset = datetime.strftime(self.calculate_end_this_month(), "%Y-%m-%d")

	def action(self, logs):
		return self.for_json()

	def load_map_entity(self):
		if (self.type == "google_maps"):
			return GoogleMapsProvider(image_provider_entity=self)
		if (self.type == "mapbox"):
			return MapboxProvider(image_provider_entity=self)
		if (self.type == "ahn"):
			return AhnProvider(image_provider_entity=self)

	def calculate_end_this_month(self):
		temp_today = datetime.today()
		temp_month = temp_today.month
		temp_year = temp_today.year
		temp_end = monthrange(temp_year, temp_month)
		return str(temp_year) + "-" + str(temp_month) + "-" + str(temp_end[1])
