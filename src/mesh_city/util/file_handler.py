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
			"resource_path":
			Path.joinpath(self.root, 'resources'),
			"image_path":
			Path.joinpath(self.root, 'resources', 'images'),
			"users.json":
			Path.joinpath(self.root, 'resources', 'user', 'users.json'),
			"biome_index":
			Path.joinpath(self.root, 'resources', 'PlanetPainter_BiomeIndex.csv'),
			"MVRDV":
				Path.joinpath(self.root, 'resources', 'mvrdv', 'mvrdv_logo.png')
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
