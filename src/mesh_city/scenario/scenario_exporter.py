"""
See :class:`.RequestExporter`
"""
import csv
import math
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
from shapely.geometry import Polygon

from mesh_city.request.entities.request import Request
from mesh_city.request.entities.tile import Tile
from mesh_city.request.layers.cars_layer import CarsLayer
from mesh_city.request.layers.google_layer import GoogleLayer
from mesh_city.request.layers.layer import Layer
from mesh_city.request.layers.trees_layer import TreesLayer
from mesh_city.request.request_exporter import RequestExporter
from mesh_city.request.request_manager import RequestManager
from mesh_city.scenario.scenario import Scenario
from mesh_city.util.geo_location_util import GeoLocationUtil


class ScenarioExporter:
	"""
	An exporter for requests that exports selected layers.
	"""

	def __init__(self, request_manager: RequestManager, overlay_image: Image):
		self.request_manager = request_manager
		self.overlay_image = overlay_image

	def render_tile(self, tile: Tile, scenario: Scenario) -> Image:
		"""
		Renders an image tile at full resolution for a given scenario.
		:param tile: The tile to modify as part of the scenario
		:param buildings: The scenario to apply to the tile
		:return:
		"""
		request = scenario.request
		x_offset = (tile.x_grid_coord - request.x_grid_coord) * 1024
		y_offset = (tile.y_grid_coord - request.y_grid_coord) * 1024
		buildings = scenario.buildings.copy(deep=True)
		buildings.geometry = buildings.geometry.translate(xoff=-x_offset, yoff=-y_offset,
		                                                         zoff=0)
		base_image = Image.open(tile.path)
		green_overlay = np.asarray(self.overlay_image)
		vertical_tiles = math.ceil(base_image.height / self.overlay_image.height)
		horizontal_tiles = math.ceil(base_image.width / self.overlay_image.width)
		tiled_overlay = np.tile(green_overlay, (vertical_tiles, horizontal_tiles, 1))
		mask_base = Image.new('RGB', (base_image.width, base_image.height), (0, 0, 0))
		draw = ImageDraw.Draw(mask_base)
		for (index, (polygon, label)) in enumerate(
			zip(buildings["geometry"], buildings["label"])):
			#
			if label == "Shrubbery":
				vertices = list(zip(*polygon.exterior.coords.xy))
				draw.polygon(xy=vertices, fill=(255, 255, 255))

		final_mask = np.asarray(mask_base).astype(float) / 255
		final_overlay = cv2.multiply(final_mask, tiled_overlay, dtype=cv2.CV_32F)
		masked_numpy_base = cv2.multiply(
			1 - final_mask, np.asarray(base_image.convert("RGB")), dtype=cv2.CV_32F
		)
		new_base_image_numpy = cv2.add(masked_numpy_base, final_overlay, dtype=cv2.CV_8UC3)
		base_image = Image.fromarray(new_base_image_numpy.astype(np.uint8)).convert("RGBA")
		return base_image

	def export_scenario(self, scenario: Scenario, export_directory: Path) -> None:
		"""
		Exports a single layer from a request using methods specific to the type of the layer.

		:param request: The request that contains the layer to be exported
		:param index: The index of the layer that is to be exported.
		:param export_directory:  The root of the directory layers should be exported to.
		:return: None
		"""
		request = scenario.request
		google_layer = request.get_layer_of_type(GoogleLayer)
		for tile in google_layer.tiles:
			image = self.render_tile(tile=tile, scenario=scenario)
			origin_path = tile.path
			rel_path = origin_path.relative_to(self.request_manager.get_image_root())
			export_directory.joinpath(rel_path.parent).mkdir(parents=True, exist_ok=True)
			image.save(export_directory.joinpath(rel_path))
			filename_no_extension = origin_path.stem
			nw_latitude, nw_longitude = GeoLocationUtil.tile_value_to_degree(
				x_cor_tile=tile.x_grid_coord + 0.5,
				y_cor_tile=tile.y_grid_coord + 0.5,
				zoom=request.zoom,
				get_centre=False
			)
			world_file_name = filename_no_extension + ".pgw"
			RequestExporter.create_world_file(
				path=export_directory.joinpath(rel_path.parent, world_file_name),
				latitude=nw_latitude,
				longitude=nw_longitude,
				zoom=request.zoom,
				width=1024,
				height=1024
			)

	def create_export_csv(self, request: Request, layer: Layer):
		"""
		Method which uses the information of the bounding box detections to create a csv file with
		the centre points of the detections, which can be used for importation to QGIS
		:param request: The request that contains the layer to be exported
		:param layer: the layer that you want to export
		:return: a path to the to be exported layer
		"""
		if isinstance(layer, TreesLayer):
			label = "trees"
		elif isinstance(layer, CarsLayer):
			label = "cars"
		else:
			raise Exception("Should be a car or tree")

		detections_export_path = self.request_manager.get_image_root().joinpath(label)
		detections_export_path.mkdir(parents=True, exist_ok=True)
		detections_export_path = detections_export_path.joinpath(
			"detections_" + str(request.request_id) + "_export.csv"
		)

		x_nw, y_nw = request.x_grid_coord, request.y_grid_coord

		csv_data = {'latitude': [], 'longitude': [], 'label': [], 'generated': []}
		with open(str(layer.detections_path), newline='') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for (index, row) in enumerate(csv_reader):
				if len(row) > 0 and index > 0:
					xmin, ymin = float(row[1]), float(row[2])
					xmax, ymax = float(row[3]), float(row[4])

					latitude, longitude = GeoLocationUtil.pixel_to_geo_coor(
						x_nw, y_nw, xmin, ymin, xmax, ymax
					)
					csv_data['latitude'].append(latitude)
					csv_data['longitude'].append(longitude)
					csv_data['label'].append(label)
					csv_data['generated'].append(0)

		pd.DataFrame(csv_data).to_csv(str(detections_export_path), index=False)

		return detections_export_path
