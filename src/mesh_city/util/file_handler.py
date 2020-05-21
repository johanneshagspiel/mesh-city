import json
from pathlib import Path

from mesh_city.user.entities.user_entity import UserEntity


class FileHandler:

	def __init__(self):
		self.root = Path(__file__).parents[1]
		self.folder_overview = {
			"resource_path": [Path.joinpath(self.root, 'resources'), "resource_path"],
			"image_path": [Path.joinpath(self.root, 'resources', 'images'), "image_path"],
			"temp_path": [Path.joinpath(self.root, 'resources', 'temp'), "temp_path"],
			"users.json": [Path.joinpath(self.root, 'resources', 'user', 'users.json'), "users.json"],
			"log_request_.json":
			[Path.joinpath(self.root, 'resources', 'logs', 'log_request_.json'), "log_request_.json"],
			"active_request_path":
			[Path.joinpath(self.root, 'resources', 'images', "request_0"), "active_request_path"],
			"active_tile_path":
			[
			Path.joinpath(self.root, 'resources', 'images', "request_0", "0_tile_0_0"),
			"active_tile_path"
			],
			"active_image_path":
			[
			Path.joinpath(self.root, 'resources', 'images', "request_0", "0_tile_0_0"),
			"active_tile_path"
			],
			"active_layer_path":
			[
			Path.joinpath(self.root, 'resources', 'images', "request_0", "0_tile_0_0", "layers"),
			"active_layer_path"
			],
			"selected_layer_path":
			[
			Path.joinpath(self.root, 'resources', 'images', "request_0", "0_tile_0_0", "layers"),
			"selected_layer_path"
			]
		}

	def change(self, path_of_interest, new_location):
		self.folder_overview[path_of_interest][0] = new_location
