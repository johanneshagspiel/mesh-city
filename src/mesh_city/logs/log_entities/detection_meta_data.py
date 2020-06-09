"""
A module of the detection meta class
"""
from mesh_city.logs.log_entities.log_entity import LogEntity


class DetectionMetaData(LogEntity):
	"""
	The log entity that stores meta information
	"""

	def __init__(self, path_to_store, json=None):
		super().__init__(path_to_store=path_to_store)
		if json is None:
			self.information = {}
		else:
			self.information = {}
			self.load_json(json)

	def action(self, logs):
		"""
		What to do when log manager calls write log
		:param logs:
		:return:
		"""
		return self.for_json()

	def load_json(self, json):
		"""
		How to load the class from json
		:param json: the json file from which to log the class from
		:return: nothing (the fields are all set correctly)
		"""
		self.information = json

	def for_json(self):
		"""
		Turns the class into a json compliant form
		:return: the class in json compliant form
		"""
		return self.information
