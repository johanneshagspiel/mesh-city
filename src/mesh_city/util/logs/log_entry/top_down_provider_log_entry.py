from mesh_city.util.logs.log_entry.log_entity import LogEntity


class TopDownProviderLogEntity(LogEntity):
	"""
	Log entries created for one request by a TopDownImageryProvider and stored in the overeall request log
	"""

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
		nickname=None,
	):
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
		if nickname is None:
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
			"tile_information": self.coordinates,
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
