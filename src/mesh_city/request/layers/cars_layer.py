"""
See :class:`.CarsLayer`
"""

from pathlib import Path

from mesh_city.request.layers.layer import Layer


class CarsLayer(Layer):
	"""
	A layer class representing car detections for a request
	"""

	def __init__(self, width: int, height: int, detections_path: Path) -> None:
		self.detections_path = detections_path
		super().__init__(width, height)
