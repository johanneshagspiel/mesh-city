from pathlib import Path


class Tile:
	"""
	A 
	"""
	def __init__(self, path: Path, x_coord: int, y_coord: int) -> None:
		self.path = path
		self.x_coord = x_coord
		self.y_coord = y_coord
