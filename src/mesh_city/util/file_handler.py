"""
Module containing preliminary file handler
"""
from pathlib import Path


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
			"resource_path":
			self.root.joinpath("resources"),
			"image_path":
			self.root.joinpath("resources", "images"),
			"temp_path":
			self.root.joinpath("resources", "temp"),
			"users.json":
			self.root.joinpath("resources", "user", "users.json"),
			"coordinate_overview.json":
			self.root.joinpath("resources", "images", "coordinate_overview.json"),
			"log_request_.json":
			self.root.joinpath("resources", "logs", "log_request_.json"),
			"active_request_path":
			self.root.joinpath("resources", "images", "request_0"),
			"active_image_path":
			self.root.joinpath("resources", "images", "request_0", "0_tile_0_0"),
			"active_information_path":
			self.root.joinpath("resources", "temp", "meta"),
			"active_raw_data_path":
			self.root.joinpath("resources", "images", "request_0"),
			"active_map_path":
			self.root.joinpath("resources", "images", "request_0"),
			"active_overlay_path":
			self.root.joinpath("resources", "images", "request_0"),
			"active_meta_path":
			self.root.joinpath("resources", "images", "request_0"),
			"temp_image_path":
			self.root.joinpath("resources", "temp", "image"),
			"temp_map_path":
			self.root.joinpath("resources", "temp", "map"),
			"temp_overlay_path":
			self.root.joinpath("resources", "temp", "overlay"),
			"temp_detection_path":
			self.root.joinpath("resources", "temp", "detection"),
			"temp_meta_path":
			self.root.joinpath("resources", "temp", "meta"),
			"active_tile_path":
			self.root.joinpath("resources", "images", "request_0", "0_tile_0_0"),
			"active_layer_path":
			self.root.joinpath("resources", "images", "request_0", "0_tile_0_0", "layers"),
			"selected_layer_path":
			self.root.joinpath("resources", "images", "request_0", "0_tile_0_0", "layers"),
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
		self.folder_overview[path_of_interest] = new_location
