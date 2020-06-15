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
			"temp_path":
			Path.joinpath(self.root, 'resources', 'temp'),
			"users.json":
			Path.joinpath(self.root, 'resources', 'user', 'users.json'),
			"coordinate_overview.json":
			Path.joinpath(self.root, 'resources', 'images', 'coordinate_overview.json'),
			"log_request_.json":
			Path.joinpath(self.root, 'resources', 'logs', 'log_request_.json'),
			"active_request_path":
			Path.joinpath(self.root, 'resources', 'images', "request_0"),
			"active_image_path":
			Path.joinpath(self.root, 'resources', 'temp', 'image'),
			"active_information_path":
			Path.joinpath(self.root, 'resources', 'temp', 'meta'),
			"active_raw_data_path":
			Path.joinpath(self.root, 'resources', 'images', "request_0"),
			"active_map_path":
			Path.joinpath(self.root, 'resources', 'images', "request_0"),
			"active_overlay_path":
			Path.joinpath(self.root, 'resources', 'images', "request_0"),
			"active_meta_path":
			Path.joinpath(self.root, 'resources', 'images', "request_0"),
			"temp_image_path":
			Path.joinpath(self.root, 'resources', 'temp', 'image'),
			"temp_map_path":
			Path.joinpath(self.root, 'resources', 'temp', 'map'),
			"temp_overlay_path":
			Path.joinpath(self.root, 'resources', 'temp', 'overlay'),
			"temp_detection_path":
			Path.joinpath(self.root, 'resources', 'temp', 'detection'),
			"temp_meta_path":
			Path.joinpath(self.root, 'resources', 'temp', 'meta'),
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
