# pylint: disable=E1101,R0201,missing-class-docstring,missing-function-docstring
"""
See :class:`.RequestMaker`
"""

from pathlib import Path
from typing import Any, List, Optional, Tuple

from mesh_city.imagery_provider.top_down_provider.top_down_provider import TopDownProvider
from mesh_city.request.google_layer import GoogleLayer
from mesh_city.request.request import Request
from mesh_city.request.request_manager import RequestManager
from mesh_city.request.tile import Tile
from mesh_city.util.geo_location_util import GeoLocationUtil


class RequestMaker:
	"""
	This class makes requests to the TopDownProvider it is provided with and populates the grid system
	of its RequestManager.
	"""

	def __init__(self, request_manager: RequestManager, top_down_provider: TopDownProvider = None):
		self.request_manager = request_manager
		self.top_down_provider = top_down_provider

	@staticmethod
	def compute_3x3_area(latitude: float, longitude: float, zoom: int) -> Tuple[
		float, float, float, float]:
		"""
		This computes the bottom and top latitude, and left and right longitude that define the 3x3 tile
		grid around the point (normalized to the grid).

		:param latitude: the latitude of the coordinate
		:param longitude: the longitude of the coordinate
		:param zoom: the zoom level that defines the dimension of the tiles
		:return: The bottom and top latitude and left and right longitude defining the 3x3 tile grid.
		"""

		latitude, longitude = GeoLocationUtil.normalise_coordinates(
			latitude=latitude, longitude=longitude, zoom=zoom
		)
		bottom = GeoLocationUtil.calc_next_location_latitude(
			latitude=latitude, longitude=longitude, zoom=zoom, direction=False
		)
		top = GeoLocationUtil.calc_next_location_latitude(
			latitude=latitude, longitude=longitude, zoom=zoom, direction=True
		)
		right = GeoLocationUtil.calc_next_location_longitude(
			latitude=latitude, longitude=longitude, zoom=zoom, direction=True
		)
		left = GeoLocationUtil.calc_next_location_longitude(
			latitude=latitude, longitude=longitude, zoom=zoom, direction=False
		)
		return bottom, left, top, right

	def set_top_down_provider(self, top_down_provider: TopDownProvider) -> None:
		"""
		Sets the top down provider. This is required before any requests can be made.

		:param top_down_provider: the top_down_provider that should be used when making requests
		:return:
		"""
		self.top_down_provider = top_down_provider

	def check_zoom(self, zoom: Optional[int]) -> int:
		"""
		Checks if the zoom value is a legal value and corrects it if it is not.

		:param zoom: the zoom value that has to be checked and clamped
		:return: a legal zoom value
		"""

		assert self.top_down_provider is not None

		result_zoom: int
		if zoom is None:
			result_zoom = self.top_down_provider.max_zoom
		elif zoom < 1:
			result_zoom = 1
		elif zoom > self.top_down_provider.max_zoom:
			result_zoom = self.top_down_provider.max_zoom
		else:
			result_zoom = zoom
		return result_zoom

	def make_single_request(self, tile_x: int, tile_y: int, folder_path: Path, zoom: int) -> Tile:
		"""
		Makes a single request using the TopDownProvider that is set for a certain tile, and returns
		a corresponding tile with a reference to the imagery downloaded by the provider.

		:param tile_x: The x coordinate on the tile grid
		:param tile_y: The y coordinate on the tile grid
		:param folder_path: The folder path where the tile should be saved
		:param zoom: The zoom level
		:return: A tile with a Path to the stored image.
		"""

		assert self.top_down_provider is not None

		if self.request_manager.is_in_grid(tile_x, tile_y):
			return self.request_manager.get_tile_from_grid(tile_x, tile_y)
		file_name = str(tile_x) + "_" + str(tile_y) + ".png"
		latitude, longitude = GeoLocationUtil.tile_value_to_degree(tile_x, tile_y, zoom)
		result_path = self.top_down_provider.get_and_store_location(
			latitude=latitude,
			longitude=longitude,
			zoom=zoom,
			filename=file_name,
			new_folder_path=folder_path,
		)
		return Tile(path=result_path, x_grid_coord=tile_x, y_grid_coord=tile_y)

	def make_area_request(
		self,
		bottom_latitude: float,
		left_longitude: float,
		top_latitude: float,
		right_longitude: float,
		zoom: Any = None
	) -> Request:
		"""
		Creates a request with a GoogleLayer populated with tiles retrieved using the top down provider.

		:param bottom_latitude: The bottom-most latitude value
		:param left_longitude: The leftmost longitude value
		:param top_latitude: The top-most latitude value
		:param right_longitude: The rightmost longitude value
		:param zoom: The zoom level, can be None
		:return: The request object with a populated GoogleLayer
		"""

		if self.top_down_provider is None:
			raise Exception("The top down provider has not been set, no request could be made")
		zoom = self.check_zoom(zoom=zoom)
		coordinates, width, height = self.calculate_coordinates_for_rectangle(
			bottom_latitude=bottom_latitude,
			left_longitude=left_longitude,
			top_latitude=top_latitude,
			right_longitude=right_longitude,
			zoom=zoom
		)
		tiles = []
		folder = Path.joinpath(self.request_manager.get_image_root(), "google_maps")
		folder.mkdir(parents=True, exist_ok=True)
		min_x = None
		min_y = None
		for (x_cor_tile, y_cor_tile) in coordinates:
			if min_x is None:
				min_x = x_cor_tile
				min_y = y_cor_tile
			min_x = min(min_x, x_cor_tile)
			min_y = min(min_y, y_cor_tile)
			request_result = self.make_single_request(x_cor_tile, y_cor_tile, folder, zoom)
			tiles.append(request_result)
		request = Request(
			x_grid_coord=min_x,
			y_grid_coord=min_y,
			request_id=self.request_manager.get_new_request_id(),
			num_of_horizontal_images=width,
			num_of_vertical_images=height,
			zoom=zoom
		)
		request.add_layer(
			GoogleLayer(
			width=request.num_of_horizontal_images,
			height=request.num_of_vertical_images,
			tiles=tiles
			)
		)
		return request

	def calculate_coordinates_for_location(
		self,
		latitude: float,
		longitude: float,
		zoom: Any = None
	) -> Tuple[List[Tuple[int, int]], int, int]:
		"""
		Calculates a 3x3 section of tiles around a given point defined by a latitude and longitude.

		:param latitude: The latitude value the 3x3 section is centred at
		:param longitude: The longitude value the 3x3 section is centred at
		:param zoom: The zoom value
		:return: A list of tuples defining grid-coordinates defining the 3x3 section together with
		the width and height of the section, so always 3, 3.
		"""

		zoom = self.check_zoom(zoom)
		bottom, left, top, right = RequestMaker.compute_3x3_area(latitude, longitude, zoom)
		return self.calculate_coordinates_for_rectangle(bottom, left, top, right, zoom)

	def make_location_request(self, latitude: float, longitude: float, zoom: Any = None) -> Request:
		"""
		Creates a request with a GoogleLayer populated with tiles retrieved using the top down provider
		by first calculating a 3x3 section of tiles around a given point defined by a latitude and
		longitude.

		:param latitude: The latitude value the 3x3 section is centred at
		:param longitude: The longitude value the 3x3 section is centred at
		:param zoom: The zoom level, can be None
		:return: The request object with a populated GoogleLayer
		"""

		zoom = self.check_zoom(zoom)
		bottom, left, top, right = RequestMaker.compute_3x3_area(latitude, longitude, zoom)
		return self.make_area_request(bottom, left, top, right, zoom)

	def calculate_coordinates_for_rectangle(
		self,
		bottom_latitude: float,
		left_longitude: float,
		top_latitude: float,
		right_longitude: float,
		zoom: Any = None
	) -> Tuple[List[Tuple[int, int]], int, int]:
		"""
		Calculates the grid coordinates corresponding to a rectangle defined by two latitude,
		longitude pairs.

		:param bottom_latitude: The bottom-most latitude value
		:param left_longitude: The leftmost longitude value
		:param top_latitude: The top-most latitude value
		:param right_longitude: The rightmost longitude value
		:param zoom: The zoom value
		:return: A list of grid-coordinate tuples together with the width and height of the tile grid
		these coordinates make up.
		"""

		zoom = self.check_zoom(zoom)
		(bottom_latitude, left_longitude), (top_latitude,
			right_longitude) = GeoLocationUtil.get_bottom_left_top_right_coordinates(
			(bottom_latitude, left_longitude), (top_latitude, right_longitude)
			)
		# normalise coordinate input before adding it to coordinate list
		latitude_first_image, longitude_first_image = GeoLocationUtil.normalise_coordinates(
			bottom_latitude, left_longitude, zoom)
		current_latitude, current_longitude = latitude_first_image, longitude_first_image

		coordinates_list = []
		num_of_images_horizontal = 0
		num_of_images_vertical = 0
		# iterate from left to right, bottom to top
		while current_latitude <= top_latitude or current_latitude == 0:
			num_of_images_horizontal = 0
			while current_longitude <= right_longitude or current_longitude == 0:
				x_cor_current_tile, y_cor_current_tile = GeoLocationUtil.degree_to_tile_value(
					current_latitude, current_longitude, zoom
				)
				coordinates_list.append((x_cor_current_tile, y_cor_current_tile))
				current_longitude = GeoLocationUtil.calc_next_location_longitude(
					current_latitude, current_longitude, zoom, True
				)
				num_of_images_horizontal += 1
			current_longitude = longitude_first_image
			current_latitude = GeoLocationUtil.calc_next_location_latitude(
				current_latitude, current_longitude, zoom, True
			)
			num_of_images_vertical += 1
		coordinates_list = sorted(coordinates_list, key=lambda coordinate: coordinate[1])
		return coordinates_list, num_of_images_horizontal, num_of_images_vertical

	def count_uncached_tiles(self, coordinates: List[Tuple[int, int]]) -> int:
		"""
		Computes how many new tiles will have to be downloaded from the provider.

		:param coordinates: The list of coordinate tuples to check.
		:return: How many images are to be downloaded
		"""

		counter = 0
		for (latitude, longitude) in coordinates:
			if not self.request_manager.is_in_grid(latitude, longitude):
				counter += 1
		return counter
