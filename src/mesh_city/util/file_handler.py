"""
Module containing preliminary file handler
"""

from pathlib import Path
from mesh_city.logs.log_entities.coordinate_overview import CoordinateOverview

class FileHandler:
	"""
	Preliminary filehanler class that stores all the information surrounding paths
	"""

	def __init__(self, root=None):
		"""
		Creates a dictionary of name to (path, name). Name is needed in the tuple so that a method
		can now where it is
		"""

		self.root = root
		if root is None:
			self.root = Path(__file__).parents[1]
		self.folder_overview = {
			"resource_path": [Path.joinpath(self.root, 'resources'), "resource_path"],
			"image_path": [Path.joinpath(self.root, 'resources', 'images'), "image_path"],
			"temp_path": [Path.joinpath(self.root, 'resources', 'temp'), "temp_path"],
			"users.json": [Path.joinpath(self.root, 'resources', 'user', 'users.json'), "users.json"],
			"coordinate_overview.json": [Path.joinpath(self.root, 'resources', 'images', 'coordinate_overview.json'), "coordinate_overview.json"],
			"log_request_.json": [Path.joinpath(self.root, 'resources', 'logs', 'log_request_.json'), "log_request_.json"],
			"active_request_path": [Path.joinpath(self.root, 'resources', 'images', "request_0"), "active_request_path"],
			"temp_image_path" : [Path.joinpath(self.root, 'resources', 'temp', 'image'), 'temp_image_path'],
			"temp_map_path": [Path.joinpath(self.root, 'resources', 'temp', 'map'), 'temp_map_path'],
			"temp_overlay_path": [Path.joinpath(self.root, 'resources', 'temp', 'overlay'), 'temp_overlay_path'],
			"active_tile_path":[Path.joinpath(self.root, 'resources', 'images', "request_0", "0_tile_0_0"), "active_tile_path"],
			"active_image_path": [Path.joinpath(self.root, 'resources', 'images', "request_0", "0_tile_0_0"),"active_tile_path"],
			"active_layer_path": [Path.joinpath(self.root, 'resources', 'images', "request_0", "0_tile_0_0", "layers"), "active_layer_path"],
			"selected_layer_path": [Path.joinpath(self.root, 'resources', 'images', "request_0", "0_tile_0_0", "layers"), "selected_layer_path"]
		}
		self.coordinate_overview = None

	def change(self, path_of_interest, new_location):
		"""
		Preliminary method to unify all changes of a path in the file_handler so that they can be
		changed more easily later on
		:param path_of_interest: what to change
		:param new_location: what to change it to
		:return: nothing (updates path dictionary)
		"""
		self.folder_overview[path_of_interest][0] = new_location

