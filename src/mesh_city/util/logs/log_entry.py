"""
A module that contains all the different kinds of log entries used in this project
"""
from datetime import datetime as dt
from abc import ABC, abstractmethod

class LogEntry(ABC):
	"""
	An abstract logentry class that every instance of a log entry needs to correspond to
	"""

	def __init__(self, path_to_store):
		"""
		The initialization method. Sets the path to store the log
		:param path_to_store: where to store the log
		"""
		self.path_to_store = path_to_store
		pass

		@abstractmethod
		def for_json(self):
			"""
			Turns one log entry into a form that can be stored as a json
			:param self: the object to be stored as a json
			:return: a json compliant string
			"""
			pass

		@abstractmethod
		def action(self, logs):
			"""
			Performs an action associated with this log i.e. adding a new entry to a log
			:param self: the log entry to be added to some larger log
			:param logs: the larger log entry to be added to
			:return: nothing
			"""
			pass

class TopDownProviderLogEntry(LogEntry):
	"""
	Log entries created for one request by a TopDownImageryProvider and stored in the overeall request log
	"""

	def __init__(
		self, path_to_store, request_number, zoom_level, user_info, map_entity, number_requests,
		bounding_box, coordinates, nickname = None):
		"""
		Initializes fields of a TopDownProviderLogEntry
		:param path_to_store: where to store the log
		:param request_number: the number of the request for which to create a log
		:param zoom_level: the zoom level used for this request
		:param user_info: the user who made this request
		:param map_entity: the map entity used for this request
		:param number_requests: how many individual requests for an image have been made in this request
		:param bounding_box: the bounding_box encompassing are requested
		:param coordinates: the requests of all the individual map requests
		:param nickname: a nickname given to the request to easier identify the request i.e. Rotterdam
		"""
		super().__init__(path_to_store)

		self.request_number = str(request_number)
		self.name_user = str(user_info.name)
		if(nickname == None):
			self.nickname = ""
		else:
			self.nickname = str(nickname)
		self.zoom_level = str(zoom_level)
		self.map_provider = str(map_entity.name)
		self.number_requests = str(number_requests)
		self.date = str(dt.now().day) + "/" + str(dt.now().month) + "/" + str(
			dt.now().year
		) + ", " + str(dt.now().hour) + ":" + str(dt.now().minute)
		self.bounding_box = str(bounding_box)
		self.coordinates = str(coordinates)

	def for_json(self):
		"""
		Makes the object ready to be stored as a json file
		:return: json complying string
		"""
		return {
			self.request_number : {
				"nickname" : self.nickname,
				"name_user": self.name_user,
				"zoom_level" : self.zoom_level,
				"map_provider": self.map_provider,
				"number_requests": self.number_requests,
				"date": self.date,
				"bounding_box": self.bounding_box,
				"coordinates": self.coordinates,
			}
		}  # yapf: disable

	def action(self, logs):
		"""
		Adds the object at the appropriate field to the log
		:param logs: the logs to add the object to
		:return: json file to be stored with the added entry
		"""
		temp_result = logs["top_down_provider"].append(self.for_json())
		return temp_result


class TopDownProviderRequestLog(LogEntry):
	"""
	Meta information for one request
	"""

	def __init__(self, path_to_store, starting_location, max_latitude,
	             max_longitude, max_zoom, layers):
		"""
		Initializes a log entry to store meta information about a request
		:param path_to_store: where to store the log
		:param starting_location: which tile to load first in the map
		:param max_latitude: maximum latitude of a request
		:param max_longitude: max longitude of a request
		:param max_zoom: max zoom level usable for this request
		:param layers: the layers that exist for this request
		"""
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
				"max_latitude": self.name_user,
				"max_longitude": self.map_provider,
				"max_zoom": self.number_requests,
				"layers" : self.layers
			}  # yapf: disable

		def action(self, logs):
			"""
			Makes the action appropriate for this type of log
			:param self: the object to be stored
			:param logs: the logs to add the object to
			:return: object to be stored in a json file
			"""
			return self.for_json()
