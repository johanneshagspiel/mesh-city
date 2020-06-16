"""
See :class:`.Scenario`
"""

from abc import ABC


class Scenario(ABC):
	"""
	An abstract base class that request scenarios inherit from.
	"""

	def __init__(self, scenario_name: str, width: int, height: int) -> None:
		self.scenario_name = scenario_name
		self.width = width
		self.height = height
