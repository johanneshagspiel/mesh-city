"""
See :class:`.MoreTreesScenario`
"""

from pathlib import Path

from mesh_city.request.scenario.scenario import Scenario


class MoreTreesScenario(Scenario):
	"""
	A layer class representing the more trees scenario for a request
	"""

	def __init__(self, scenario_index: int, width: int, height: int, scenario_path: Path) -> None:
		self.scenario_path = scenario_path
		super().__init__(scenario_index, width, height)
