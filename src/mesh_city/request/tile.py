"""
See :class:`.Tile`
"""
from pathlib import Path


class Tile:
	"""
	A class representing an image from the image grid maintained by RequestManager.
	"""

	def __init__(self, path: Path, x_coord: int, y_coord: int) -> None:
		self.path = path
		self.x_coord = x_coord
		self.y_coord = y_coord
