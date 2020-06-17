"""
See :class:`.Scenario`
"""
from pathlib import Path


class Scenario:
	"""
	An the base scenario class.
	"""

	def __init__(
		self, scenario_name: str, width: int, height: int, scenario_path: Path, information_path: Path
	) -> None:
		self.scenario_name = scenario_name
		self.width = width
		self.height = height
		self.scenario_path = scenario_path
		self.information_path = information_path
