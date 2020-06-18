"""
See :class:`.ScenarioBuilder`
"""
from mesh_city.request.entities.request import Request


class ScenarioBuilder:
	"""
	A class used to create scenario's from requests whose behaviour can be customized by specifying
	what type of things it should change.
	"""

	def __init__(
		self,
	):
		pass

	def get_possible_scenarios(self, request: Request):
		layer_set = set()
		for layer in request.layers:
			layer_set.add(type(layer))

