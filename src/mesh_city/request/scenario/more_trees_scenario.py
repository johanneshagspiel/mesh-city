"""
See :class:`.MoreTreesScenario`
"""

from pathlib import Path

from mesh_city.request.scenario.scenario import Scenario


class MoreTreesScenario(Scenario):
	"""
	A layer class representing the more trees scenario for a request
	"""

	def __init__(self, width: int, height: int, detections_path: Path) -> None:
		self.detections_path = detections_path
		super().__init__(width, height)
