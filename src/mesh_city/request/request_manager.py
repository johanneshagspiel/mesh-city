"""
See :class:`.RequestManager`
"""

import json
import os
from pathlib import Path

from mesh_city.request.entities.request import Request
from mesh_city.request.entities.tile import Tile
from mesh_city.request.layers.buildings_layer import BuildingsLayer
from mesh_city.request.layers.cars_layer import CarsLayer
from mesh_city.request.layers.google_layer import GoogleLayer
from mesh_city.request.layers.trees_layer import TreesLayer
from mesh_city.request.scenario.more_trees_scenario import MoreTreesScenario


class RequestManager:
	"""A class for storing previous requests and reusing their imagery"""

	def __init__(self, image_root):
		self.__images_root = image_root
		self.__grid = {}
		self.requests = []

	def load_data(self) -> None:
		"""
		Builds up grid of references to imagery discovered on disk and deserializes stored requests.

		:return: None
		"""

		self.discover_old_imagery()
		self.deserialize_requests()

	def discover_old_imagery(self) -> None:
		"""
		Checks if the image root already contains downloaded images and loads these into the grid if so.

		:return: None
		"""

		google_folder = self.__images_root.joinpath("google_maps")
		if google_folder.exists():
			file_paths = sorted(google_folder.glob('*.png'))
			for path in file_paths:
				rel_path = Path(path).relative_to(google_folder)
				path_no_ex = os.path.splitext(rel_path)[0]
				numbers = [int(s) for s in path_no_ex.split('_')]
				self.add_tile_to_grid(
					numbers[0],
					numbers[1],
					Tile(path=path, x_grid_coord=numbers[0], y_grid_coord=numbers[1])
				)

	def serialize_requests(self) -> None:
		"""
		Serializes the requests to a JSON file.

		:return: None
		"""

		request_list = []
		for request in self.requests:
			request_list.append(
				{
				"request_id": request.request_id,
				"x_grid_coord": request.x_grid_coord,
				"y_grid_coord": request.y_grid_coord,
				"num_of_horizontal_images": request.num_of_horizontal_images,
				"num_of_vertical_images": request.num_of_vertical_images,
				"zoom": request.zoom
				}
			)
		with open(self.__images_root.joinpath("requests.json"), 'w') as fout:
			json.dump(request_list, fout)

	def deserialize_requests(self) -> None:
		"""
		Deserializes requests from a set JSON file.

		:return: None
		"""

		if self.__images_root.joinpath("requests.json").exists():
			with open(self.__images_root.joinpath("requests.json"), "r") as read_file:
				data = json.load(read_file)
				for request_json in data:
					request = Request(**request_json)
					tiles = []
					for y_offset in range(request.num_of_vertical_images):
						for x_offset in range(request.num_of_horizontal_images):
							tile_x = request.x_grid_coord + x_offset
							tile_y = request.y_grid_coord + y_offset
							tiles.append(self.get_tile_from_grid(tile_x, tile_y))
					request.add_layer(
						GoogleLayer(
						width=request.num_of_horizontal_images,
						height=request.num_of_vertical_images,
						tiles=tiles
						)
					)
					tree_detections_path = self.__images_root.joinpath(
						"trees", "detections_" + str(request.request_id) + ".csv"
					)
					if tree_detections_path.exists():
						request.add_layer(
							TreesLayer(
							width=request.num_of_horizontal_images,
							height=request.num_of_vertical_images,
							detections_path=tree_detections_path
							)
						)
					car_detections_path = self.__images_root.joinpath(
						"cars", "detections_" + str(request.request_id) + ".csv"
					)
					if car_detections_path.exists():
						request.add_layer(
							CarsLayer(
							width=request.num_of_horizontal_images,
							height=request.num_of_vertical_images,
							detections_path=car_detections_path
							)
						)
					building_detections_path = self.__images_root.joinpath(
						"buildings", "detections_" + str(request.request_id) + ".geojson"
					)
					if building_detections_path.exists():
						request.add_layer(
							BuildingsLayer(
							width=request.num_of_horizontal_images,
							height=request.num_of_vertical_images,
							detections_path=building_detections_path
							)
						)
					more_trees_path = self.__images_root.joinpath("more_trees")
					if more_trees_path.exists():
						pattern = "request" + str(request.request_id) + "*"
						file_paths = sorted(more_trees_path.glob(pattern))
						for file_path in file_paths:
							scenario_name = str(file_path).split("_")[1]
							request.add_scenario(
								MoreTreesScenario(
									scenario_name=scenario_name,
									width=request.num_of_horizontal_images,
									height=request.num_of_vertical_images,
									detections_path=file_path
								)
							)

					self.add_request(request=request)

	def add_request(self, request: Request) -> None:
		"""
		Adds a new request to this manager and updates the grid accordingly.

		:param request: The request that is to be added to the manager.
		:return: None
		"""

		self.requests.append(request)
		self.update_grid(request)

	def get_new_request_id(self) -> int:
		"""
		Gets a new unused request id.

		:return: An unused request id.
		"""

		if self.requests:
			return max(request.request_id for request in self.requests) + 1
		return 0

	def get_request_by_id(self, index: int) -> Request:
		"""
		Gets a request by id.

		:param index: The id to look for.
		:return: A Request if one with this id exists, else raises a ValueError
		"""

		for request in self.requests:
			if request.request_id is index:
				return request
		raise ValueError("No request with this id exists")

	def get_image_root(self) -> Path:
		"""
		Returns the root of the filesystem this request manager maintains and reads from.

		:return: The root
		"""
		return self.__images_root

	def update_grid(self, request: Request) -> None:
		"""
		Updates a grid by adding any tiles from the GoogleLayer of a Request that are not in the grid
		yet.

		:param request: The request to extract tiles from.
		:return: None
		"""

		if request.has_layer_of_type(GoogleLayer):
			google_layer = request.get_layer_of_type(GoogleLayer)
			for tile in google_layer.tiles:
				if not self.is_in_grid(tile.x_grid_coord, tile.y_grid_coord):
					self.add_tile_to_grid(tile.x_grid_coord, tile.y_grid_coord, tile)

	def is_in_grid(self, x_coord: int, y_coord: int) -> bool:
		"""
		Checks if a tile with these coordinates exists in the grid.

		:param x_coord: The x coordinate
		:param y_coord: The y coordinate
		:return: True if such a tile exists, False otherwise.
		"""
		return x_coord in self.__grid and y_coord in self.__grid[x_coord]

	def add_tile_to_grid(self, x_coord: int, y_coord: int, tile: Tile) -> None:
		"""
		Adds a tile to the grid and updates the internal grid dictionary accordingly.

		:param x_coord: The x coordinate
		:param y_coord: The y coordinate
		:param tile: The Tile object to add.
		:return: None
		"""

		if not x_coord in self.__grid:
			self.__grid[x_coord] = {}
		self.__grid[x_coord][y_coord] = tile

	def get_tile_from_grid(self, x_coord: int, y_coord: int) -> Tile:
		"""
		Gets a Tile from the grid if it exists at these coordinates

		:param x_coord: The x coordinate
		:param y_coord: The y coordinate
		:return: A tile if it is found, a ValueError otherwise.
		"""

		if not self.is_in_grid(x_coord=x_coord, y_coord=y_coord):
			raise ValueError("There is no tile in the grid with these coordinates")
		return self.__grid[x_coord][y_coord]
