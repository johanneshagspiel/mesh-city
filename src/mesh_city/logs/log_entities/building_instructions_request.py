"""
See :class:`.TopDownProviderRequestLog`
"""

from mesh_city.logs.log_entities.log_entity import LogEntity


class BuildingInstructionsRequest(LogEntity):

	def __init__(self, path_to_store, json=None):
		super().__init__(path_to_store=path_to_store)
		if json is None:
			self.instructions ={}
		else:
			self.instructions = {}
			self.load_json(json)

	def action(self, logs):
		return self.for_json()

	def load_json(self, json):
		self.instructions = json

	def for_json(self):
		return self.instructions
