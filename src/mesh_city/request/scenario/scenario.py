"""
See :class:`.Scenario`
"""

from abc import ABC


class Scenario(ABC):
	"""
	An abstract base class that request scenarios inherit from.
	"""

	def __init__(self, scenario_index: int, width: int, height: int) -> None:
		self.scenario_index = scenario_index
		self.width = width
		self.height = height
