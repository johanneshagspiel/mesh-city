"""
This module contains the image provider log
"""
from calendar import monthrange
from datetime import datetime

from mesh_city.util.logs.log_entry.log_entity import LogEntity


class ImageProviderEntity(LogEntity):
	"""
	The image provider log class that stores all information regarding one image provider associated
	with a user such as api key, usage, quota etc.
	"""

	def __init__(
		self, file_handler, type_map_provider, api_key, quota, usage=None, date_reset=None
	):
		"""
		Sets up a image provider, either from json or when created for the first time
		:param file_handler: the file handler needed to store the image provider
		:param type_map_provider: what kind of image provider this is
		:param api_key: the api key associated with the image provider
		:param quota: the quota to be observed
		:param usage: a dictionary representing the total usage, static map usage
		and geocoding usage.
		:param date_reset: The date the monthly usage should be reset.
		"""
		super().__init__(path_to_store=file_handler.folder_overview['users.json'][0])
		self.type = type_map_provider
		self.api_key = api_key
		self.usage = usage
		if usage is None:
			self.usage = {"static_map": 0, "geocoding": 0, "total": 0}
		self.quota = int(quota)
		self.date_reset = self.calculate_end_of_month(datetime.today())
		if date_reset is not None:
			self.date_reset = date_reset
			self.check_date_reset(datetime.today())

	def for_json(self):
		"""
		Turns the class into a json compliant form
		:return: the class in a json compliant form
		"""
		return {
			"type_map_provider": self.type,
			"api_key": self.api_key,
			"usage":
			{
			"static_map": self.usage["static_map"],
			"geocoding": self.usage["geocoding"],
			"total": self.usage["total"]
			},
			"quota": self.quota,
			"date_reset": self.date_reset.date().isoformat()
		}

	def check_date_reset(self, current_date):
		"""
		Checks if the usage should be reset if a new month has started
		:return: nothing (but the usage fields are reset to 0)
		"""

		if current_date >= self.date_reset:
			self.usage["static_map"] = 0
			self.usage["geocoding"] = 0
			self.usage["total"] = 0
			self.date_reset = self.calculate_end_of_month(current_date)

	# pylint: disable=W0613
	def action(self, logs):
		"""
		Action performed when called by the log manager when writing to file
		:param logs: global log context
		:return: just turns the object to json
		"""
		return self.for_json()

	@staticmethod
	def calculate_end_of_month(date):
		"""
		Helper method to calculate the end of a month
		:return: a string containing the end of the month
		"""
		temp_end = monthrange(date.year, date.month)
		return datetime(date.year, date.month, temp_end[1])
