"""
See :class:`.TopDownProviderRequestLog`
"""

from mesh_city.logs.log_entities.log_entry import LogEntry


class TopDownProviderRequestLog(LogEntry):
	"""
	Meta information for one request
	"""

	def __init__(
		self, path_to_store, json=None, starting_location = None, max_latitude = None,
		max_longitude = None, max_zoom = None, layers = None
	):

		if starting_location and max_latitude and max_longitude and max_zoom and layers is not None:

		super().__init__(path_to_store)
		self.starting_location = str(starting_location)
		self.max_latitude = str(max_latitude)
		self.max_longitude = str(max_longitude)
		self.max_zoom = str(max_zoom)
		self.layers = layers

	def for_json(self):
		"""
		Makes the object ready to be stored as a json file
		:param self: object to turn into json
		:return: a json compliant string
		"""
		return {
			"center" : self.starting_location,
			"max_latitude": self.max_latitude,
			"max_longitude": self.max_longitude,
			"max_zoom": self.max_zoom,
			"layers" : self.layers,
		}  # yapf: disable

	def action(self, logs):
		"""
		Makes the action appropriate for this type of log
		:param self: the object to be stored
		:param logs: the logs to add the object to
		:return: object to be stored in a json file
		"""
		return self.for_json()
