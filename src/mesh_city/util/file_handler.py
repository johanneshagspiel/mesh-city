"""
Module containing preliminary file handler
"""

from pathlib import Path


class FileHandler:
	"""
	Preliminary file handler class that stores all the information surrounding paths.
	"""

	def __init__(self, root=None):
		"""
		Creates a dictionary of name to (path, name). Name is needed in the tuple so that a method
		can now where it is.
		"""

		self.root = root
		if root is None:
			self.root = Path(__file__).parents[1]

		self.folder_overview = {
			"resource_path": self.root.joinpath("resources"),
			"image_path": self.root.joinpath("resources", "images"),
			"users.json": self.root.joinpath("resources", "user", "users.json"),
			"biome_index": self.root.joinpath("resources", "mvrdv", "PlanetPainter_BiomeIndex.csv"),
			"logo": self.root.joinpath("resources", "mvrdv", "planet_painter_logo.png"),
			"fonts": self.root.joinpath("resources", "fonts"),
			"icon": self.root.joinpath("resources", "mvrdv", "planet_painter_icon.ico"),
		}
		# initiated with a CoordinateOverview, coordinate_overview.grid is a json file
		self.coordinate_overview = None

	def change(self, path_of_interest, new_location):
		"""
		Preliminary method to unify all changes of a path in the file_handler so that they can be
		changed more easily later on.

		:param path_of_interest: what to change
		:param new_location: what to change it to
		:return: nothing (updates path dictionary)
		"""
		self.folder_overview[path_of_interest] = new_location
