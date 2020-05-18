from abc import ABC, abstractmethod
from datetime import datetime as dt


class LogEntry(ABC):

	def __init__(self, path_to_store):
		self.path_to_store = path_to_store
		pass

		@abstractmethod
		def for_json(self):
			pass

		@abstractmethod
		def action(self, logs):
			pass


class TopDownProviderLogEntry(LogEntry):

	def __init__(
		self,
		path_to_store,
		request_number,
		zoom_level,
		user_info,
		map_entity,
		number_requests,
		bounding_box,
		coordinates,
		nickname=None
	):
		super().__init__(path_to_store)

		self.request_number = str(request_number)
		self.name_user = str(user_info.name)
		if (nickname == None):
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
		temp_result = logs["top_down_provider"].append(self.for_json())
		return temp_result


class TopDownProviderRequestLog(LogEntry):

	def __init__(
		self, path_to_store, starting_location, max_latitude, max_longitude, max_zoom, layers
	):
		super().__init__(path_to_store)
		self.starting_location = str(starting_location)
		self.max_latitude = str(max_latitude)
		self.max_longitude = str(max_longitude)
		self.max_zoom = str(max_zoom)
		self.layers = layers

		def for_json(self):
			return {
				"center" : self.starting_location,
				"max_latitude": self.name_user,
				"max_longitude": self.map_provider,
				"max_zoom": self.number_requests,
				"layers" : self.layers
			}  # yapf: disable

		def action(self, logs):
			return self.for_json()
