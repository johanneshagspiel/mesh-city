import json
import os
from pathlib import Path

from mesh_city.request.google_layer import GoogleLayer
from mesh_city.request.request import Request
from mesh_city.request.tile import Tile
from mesh_city.request.trees_layer import TreesLayer


class RequestManager:
	"""A class for storing previous requests and reusing their imagery"""

	def __init__(self, image_root, requests=[]):
		self.requests = requests
		self.images_root = image_root
		self.grid = {}
		for request in self.requests:
			self.update_grid(request)

	def load_data(self):
		self.discover_old_imagery()
		self.deserialize_requests()

	def discover_old_imagery(self):
		google_folder = self.images_root.joinpath("google_maps")
		if google_folder.exists():
			file_paths = sorted(google_folder.glob('*.png'))
			for path in file_paths:
				rel_path = Path(path).relative_to(google_folder)
				path_no_ex = os.path.splitext(rel_path)[0]
				numbers = [int(s) for s in path_no_ex.split('_')]
				self.add_tile_to_grid(
					numbers[0], numbers[1], Tile(path=path, x_coord=numbers[0], y_coord=numbers[1])
				)

	def serialize_requests(self):
		request_list = []
		for request in self.requests:
			request_list.append(
				{
				"request_id": request.request_id,
				"x_coord": request.x_coord,
				"y_coord": request.y_coord,
				"width": request.width,
				"height": request.height,
				"zoom": request.zoom
				}
			)
		with open(self.images_root.joinpath("requests.json"), 'w') as fout:
			json.dump(request_list, fout)

	def deserialize_requests(self):
		if self.images_root.joinpath("requests.json").exists():
			with open(self.images_root.joinpath("requests.json"), "r") as read_file:
				data = json.load(read_file)
				for request_json in data:
					request = Request(**request_json)
					tiles = []
					for y_offset in range(request.height):
						for x_offset in range(request.width):
							tile_x = request.x_coord + x_offset
							tile_y = request.y_coord + y_offset
							tiles.append(self.get_tile_from_grid(tile_x, tile_y))
					request.add_layer(GoogleLayer(width=request.width,height=request.height,tiles=tiles))
					tree_detections_path = self.images_root.joinpath(
						"trees", "detections_" + str(request.request_id) + ".csv"
					)
					if tree_detections_path.exists():
						request.add_layer(TreesLayer(width=request.width,height=request.height,detections_path=tree_detections_path))
					self.add_request(request=request)

	def add_request(self, request):
		self.requests.append(request)
		self.update_grid(request)

	def get_new_request_id(self):
		return max(request.request_id for request in self.requests) + 1

	def get_request_by_id(self, id):
		for request in self.requests:
			if request.request_id is id:
				return request
		raise ValueError("No request with this id exists")

	def get_image_root(self):
		return self.images_root

	def update_grid(self, request):
		if request.has_layer_of_type(GoogleLayer):
			google_layer = request.get_layer_of_type(GoogleLayer)
			for tile in google_layer.tiles:
				if not self.is_in_grid(tile.x_coord, tile.y_coord):
					self.add_tile_to_grid(tile.x_coord, tile.y_coord, tile)

	def is_in_grid(self, latitude, longitude):
		return latitude in self.grid and longitude in self.grid[latitude]

	def add_tile_to_grid(self, latitude, longitude, tile):
		if not latitude in self.grid:
			self.grid[latitude] = {}
		self.grid[latitude][longitude] = tile

	def get_tile_from_grid(self, latitude, longitude):
		return self.grid[latitude][longitude]
