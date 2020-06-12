"""
See :class:`.TopDownProviderRequestLog`
"""

from mesh_city.logs.log_entities.log_entity import LogEntity


class BuildingInstructionsRequest(LogEntity):
	"""
	The class representing all the instructions needed to load an image and display it on the main screen
	"""

	def __init__(self, path_to_store, json=None):
		"""
		Either loads the log from a json file or creates a new, empty one.

		:param path_to_store: where to store the log
		:param json: the json file from which to load the instructions from
		"""

		super().__init__(path_to_store=path_to_store)
		if json is None:
			self.instructions = {}
		else:
			self.instructions = {}
			self.load_json(json)

	def action(self, logs):
		"""
		What to do when writing the object to file.

		:param logs: other logs where this one should be incorporated
		:return: the class as json object
		"""
		return self.for_json()

	def load_json(self, json):
		"""
		Sets up the fields based on a json file.

		:param json: the json file from which to load the data for the fields
		:return: nothing (the fields are correctly set up)
		"""
		self.instructions = json

	def for_json(self):
		"""
		Turns the class into a json compliant form.

		:return: the class in a json compliant form
		"""
		return self.instructions
