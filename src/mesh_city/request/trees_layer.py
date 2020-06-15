"""
See :class:`.TreesLayer`
"""

from pathlib import Path

from mesh_city.request.layer import Layer


class TreesLayer(Layer):
	"""
	A layer class representing tree detections for a request
	"""

	def __init__(self, width: int, height: int, detections_path: Path) -> None:
		self.detections_path = detections_path
		super().__init__(width, height)
