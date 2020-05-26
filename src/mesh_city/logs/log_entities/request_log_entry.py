"""
See :class:`.TopDownProviderRequestLog`
"""

from mesh_city.logs.log_entities.log_entry import LogEntry


class RequestLogEntry(LogEntry):
	"""
	Meta information for one request
	"""

	def __init__(
		self, path_to_store, json=None, starting_location = None, max_latitude = None,
		 tile_information = None):

		super().__init__(path_to_store=path_to_store)

		if json is not None:
			self.starting_location = None
			self.max_latitude = None
			self.tile_information = None
			self.load_json(json)

		else:
			self.starting_location = starting_location
			self.max_latitude = max_latitude
			self.tile_information = tile_information


	def for_json(self):
		"""
		Makes the object ready to be stored as a json file
		:param self: object to turn into json
		:return: a json compliant string
		"""

		temp_tile_information = {}
		for key, value in self.tile_information.items():
			temp_tile_information[key] = value.for_json()

		print(temp_tile_information)

		return {
			"starting_location" : self.starting_location,
			"max_latitude": self.max_latitude,
			"max_longitude": self.max_longitude,
			"max_zoom": self.max_zoom,
			"layers" : self.layers,
			"tile_information" : temp_tile_information
		}  # yapf: disable

	def action(self, logs):
		"""
		Makes the action appropriate for this type of log
		:param self: the object to be stored
		:param logs: the logs to add the object to
		:return: object to be stored in a json file
		"""
		return self.for_json()
