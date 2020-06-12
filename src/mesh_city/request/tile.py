"""
See :class:`.Tile`
"""

from pathlib import Path


class Tile:
	"""
	A class representing an image from the image grid maintained by RequestManager.
	"""

	def __init__(self, path: Path, x_grid_coord: int, y_grid_coord: int) -> None:
		self.path = path
		self.x_grid_coord = x_grid_coord
		self.y_grid_coord = y_grid_coord
