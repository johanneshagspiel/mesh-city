"""
See :class:`.RequestExporter`
"""

from pathlib import Path
from shutil import copyfile
from typing import List

from mesh_city.request.request import Request
from mesh_city.request.layers.buildings_layer import BuildingsLayer
from mesh_city.request.layers.cars_layer import CarsLayer
from mesh_city.request.layers.google_layer import GoogleLayer
from mesh_city.request.layers.trees_layer import TreesLayer
from mesh_city.request.request_manager import RequestManager
from mesh_city.util.geo_location_util import GeoLocationUtil


class RequestExporter:
	"""
	An exporter for requests that exports selected layers.
	"""

	def __init__(self, request_manager: RequestManager):
		self.request_manager = request_manager

	def export_request(
		self, request: Request, layer_mask: List[bool], export_directory: Path
	) -> None:
		"""
		Exports a selection of layers from a request.

		:param request: The request that is to be exported
		:param layer_mask: A list of booleans denoting which layers are to be exported
		:param export_directory: The root of the directory layers should be exported to.
		:return: None
		"""

		export_directory.mkdir(parents=True, exist_ok=True)
		for (index, flag) in enumerate(layer_mask):
			if flag:
				self.export_layer(request=request, index=index, export_directory=export_directory)

	def export_layer(self, request: Request, index: int, export_directory: Path) -> None:
		"""
		Exports a single layer from a request using methods specific to the type of the layer.

		:param request: The request that contains the layer to be exported
		:param index: The index of the layer that is to be exported.
		:param export_directory:  The root of the directory layers should be exported to.
		:return: None
		"""

		layer = request.layers[index]
		if isinstance(layer, GoogleLayer):
			for tile in layer.tiles:
				origin_path = tile.path
				rel_path = origin_path.relative_to(self.request_manager.get_image_root())
				export_directory.joinpath(rel_path.parent).mkdir(parents=True, exist_ok=True)
				copyfile(origin_path, export_directory.joinpath(rel_path))
				filename_no_extension = origin_path.stem

				nw_latitude, nw_longitude = GeoLocationUtil.tile_value_to_degree(
					x_cor_tile=tile.x_grid_coord + 0.5,
					y_cor_tile=tile.y_grid_coord + 0.5,
					zoom=request.zoom,
					get_centre=False
				)
				world_file_name = filename_no_extension + ".pgw"
				self.create_world_file(
					path=export_directory.joinpath(rel_path.parent, world_file_name),
					latitude=nw_latitude,
					longitude=nw_longitude,
					zoom=request.zoom,
					width=1024,
					height=1024
				)
		if isinstance(layer, (TreesLayer, CarsLayer)):
			origin_path = layer.detections_path
			rel_path = origin_path.relative_to(self.request_manager.get_image_root())
			export_directory.joinpath(rel_path.parent).mkdir(parents=True, exist_ok=True)
			copyfile(origin_path, export_directory.joinpath(rel_path))
		if isinstance(layer, BuildingsLayer):
			origin_path = layer.detections_path
			rel_path = origin_path.relative_to(self.request_manager.get_image_root())
			export_directory.joinpath(rel_path.parent).mkdir(parents=True, exist_ok=True)
			copyfile(origin_path, export_directory.joinpath(rel_path))

	def create_world_file(
		self, path: Path, latitude: float, longitude: float, zoom: int, width: int, height: int
	):
		"""
		Method that creates a world file for an image. World files have the same name as the image,
		but with a different extension (.pgw). World files contain the information necessary to
		export the image to GIS software such as QGIS.

		:param path: path of the file that is to be created
		:param latitude: the centre latitude of the tile
		:param longitude: the centre longitude of the tile
		:param zoom: the zoom level
		:param width: image width
		:param height: image height
		:return:
		"""

		x_tile, y_tile = GeoLocationUtil.degree_to_tile_value(
			latitude=latitude,
			longitude=longitude,
			zoom=zoom
		)
		nw_latitude, nw_longitude = GeoLocationUtil.tile_value_to_degree(
			x_cor_tile=x_tile,
			y_cor_tile=y_tile,
			zoom=zoom,
			get_centre=False
		)
		m_east_of_0, m_north_of_0 = GeoLocationUtil.transform_coordinates_to_mercator(
			latitude=nw_latitude,
			longitude=nw_longitude
		)
		pixels_per_unit_x_direction, pixels_per_unit_y_direction = GeoLocationUtil.calc_map_units_per_px_cor(
			latitude, longitude, width, height, zoom)

		with open(path, "w") as world_file:
			world_file.writelines(
				[
				str(pixels_per_unit_x_direction) + "\n",
				"0" + "\n",
				"0" + "\n",
				str(pixels_per_unit_y_direction) + "\n",
				str(m_east_of_0) + "\n",
				str(m_north_of_0)
				]
			)
