"""
A module containing the coordinate overview class
"""
from mesh_city.logs.log_entities.log_entity import LogEntity


class CoordinateOverview(LogEntity):
	"""
	The class representing the dictionary where the location is stored where one can find the image associated with a
	latitude/longitude combination
	"""

	def __init__(self, path_to_store, json=None):
		"""
		Either loads the log from a json file or creates a new, empty one. The log of all the
		previously downloaded images is dictionary named 'grid'.
		:param path_to_store: where to store the log
		:param json: the json file from which to load the instructions from
		"""
		super().__init__(path_to_store=path_to_store)
		if json is None:
			self.grid = {}
		else:
			self.grid = {}
			self.load_json(json)

	def action(self, logs):
		"""
		What to do when writing the object to file
		:param logs: other logs where this one should be incorporated
		:return: the class as json object
		"""
		return self.for_json()

	def load_json(self, json):
		"""
		Sets up the fields based on a json file
		:param json: the json file from which to load the data for the fields
		:return: nothing (the fields are correctly set up)
		"""
		self.grid = json

	def for_json(self):
		"""
		Turns the class into a json compliant form
		:return: the class in a json compliant form
		"""
		return self.grid
