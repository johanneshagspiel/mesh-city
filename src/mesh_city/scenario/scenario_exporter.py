"""
See :class:`.ScenarioExporter`
"""
import math
from pathlib import Path

import pandas as pd
from pandas import DataFrame
from PIL import Image, ImageDraw, ImageOps

from mesh_city.request.layers.google_layer import GoogleLayer
from mesh_city.request.request_exporter import RequestExporter
from mesh_city.request.request_manager import RequestManager
from mesh_city.scenario.scenario import Scenario
from mesh_city.scenario.scenario_renderer import ScenarioRenderer
from mesh_city.util.geo_location_util import GeoLocationUtil


class ScenarioExporter:
	"""
	An exporter for scenarios
	"""
	MAX_SOURCE_TREES = 10

	def __init__(self, request_manager: RequestManager, overlay_image: Image):
		self.request_manager = request_manager
		self.overlay_image = overlay_image

	def get_tree_crops(self, scenario: Scenario):
		"""
		Fetches a fixed number of images of trees from the images that make up a scenario. Assumes that not
		every detected tree is located in two seperate tiles and that at least one such tree exists
		to make the these crops be useful.
		:param scenario: The scenario to get tree crops for. Note the assumptions above.
		:return:
		"""
		trees = scenario.trees.copy(deep=True)
		source_trees = trees.loc[scenario.trees['label'] == "Tree"].copy()
		source_trees.sort_values(by="score")
		tree_crops = []
		tile_x_offset = scenario.request.x_grid_coord
		tile_y_offset = scenario.request.y_grid_coord
		for (_, row) in source_trees.iterrows():
			xmin, ymin, xmax, ymax = row["xmin"], row["ymin"], row["xmax"], row["ymax"]
			tile_xmin, tile_ymin = math.floor(row["xmin"] / 1024), math.floor(row["ymin"] / 1024)
			tile_xmax, tile_ymax = math.floor(row["xmax"] / 1024), math.floor(row["ymax"] / 1024)
			if tile_xmin == tile_xmax and tile_ymin == tile_ymax:
				# coordinates of tree within the tile
				rel_xmin = xmin - tile_xmin * 1024
				rel_ymin = ymin - tile_ymin * 1024
				rel_xmax = xmax - tile_xmin * 1024
				rel_ymax = ymax - tile_ymin * 1024
				tile_image = Image.open(
					self.request_manager.get_tile_from_grid(
					x_coord=tile_x_offset + tile_xmin, y_coord=tile_y_offset + tile_ymin
					).path
				).convert("RGBA")
				tree_image_cropped = tile_image.crop(box=(rel_xmin, rel_ymin, rel_xmax, rel_ymax))
				mask = Image.new('L', tree_image_cropped.size, 0)
				draw = ImageDraw.Draw(mask)
				draw.ellipse((0, 0) + tree_image_cropped.size, fill=255)
				source_tree_image = ImageOps.fit(
					tree_image_cropped, mask.size, centering=(0.5, 0.5)
				)
				source_tree_image.putalpha(mask)
				tree_crops.append(source_tree_image.convert("RGBA"))
				if len(tree_crops) == ScenarioExporter.MAX_SOURCE_TREES:
					break
		return tree_crops

	def get_exportable_detections(self, detections: DataFrame, tile_x_nw, tile_y_nw) -> DataFrame:
		"""
		Converts the detections that are defined by bounding boxes in pixel space to single points
		in degrees (latitude, longitude)
		:param detections: The detections to process
		:param tile_x_nw: The x coordinate in tiles of the origin of the request
		:param tile_y_nw: The y coordinate in tiles of the origin of the request
		:return: The transformed detection dataframe.
		"""
		export_data = []
		for (_, row) in detections.iterrows():
			xmin, ymin = float(row["xmin"]), float(row["ymin"])
			xmax, ymax = float(row["xmax"]), float(row["ymax"])
			latitude, longitude = GeoLocationUtil.pixel_to_geo_coor(
				tile_x_nw, tile_y_nw, xmin, ymin, xmax, ymax
			)
			export_data.append((latitude, longitude, row["label"]))
		return pd.DataFrame(export_data, columns=["latitude", "longitude", "label"])

	def export_rendering(self, scenario: Scenario, export_directory: Path) -> None:
		"""
		Exports a rendering of a given scenario to a directory.
		:param scenario: The scenario to render
		:param export_directory: The export directory
		:return: None
		"""
		request = scenario.request
		image_layer = request.get_layer_of_type(GoogleLayer)

		tree_crops = None
		if scenario.trees is not None:
			tree_crops = self.get_tree_crops(scenario=scenario)
		for tile in image_layer.tiles:
			result_image = Image.open(tile.path).convert("RGBA")
			origin_path = tile.path
			rel_path = origin_path.relative_to(self.request_manager.get_image_root())
			export_directory.joinpath(rel_path.parent).mkdir(parents=True, exist_ok=True)
			x_offset = (tile.x_grid_coord - request.x_grid_coord) * 1024
			y_offset = (tile.y_grid_coord - request.y_grid_coord) * 1024
			if scenario.trees is not None:
				trees = scenario.trees.copy(deep=True)
				trees["xmin"] -= x_offset
				trees["ymin"] -= y_offset
				trees["xmax"] -= x_offset
				trees["ymax"] -= y_offset
				if len(tree_crops) == 0:
					raise ValueError(
						"At least one cropped image of a tree is needed to render the trees, "
						"none were given"
					)
				result_image = ScenarioRenderer.render_trees_for_tile(
					base_image=result_image, trees=trees, tree_crops=tree_crops
				)
			if scenario.buildings is not None:
				buildings = scenario.buildings.copy(deep=True)
				buildings.geometry = buildings.geometry.translate(
					xoff=-x_offset, yoff=-y_offset, zoff=0
				)
				result_image = ScenarioRenderer.render_shrubbery(
					base_image=result_image,
					buildings=buildings,
					overlay_image=self.overlay_image,
					scaling=1
				)
			result_image.save(export_directory.joinpath(rel_path))
			nw_latitude, nw_longitude = GeoLocationUtil.tile_value_to_degree(
				x_cor_tile=tile.x_grid_coord + 0.5,
				y_cor_tile=tile.y_grid_coord + 0.5,
				zoom=request.zoom,
				get_centre=False
			)
			filename_no_extension = origin_path.stem
			world_file_name = filename_no_extension + ".pgw"
			RequestExporter.create_world_file(
				path=export_directory.joinpath(rel_path.parent, world_file_name),
				latitude=nw_latitude,
				longitude=nw_longitude,
				zoom=request.zoom,
				width=1024,
				height=1024
			)

	def export_scenario(self, scenario: Scenario, export_directory: Path) -> None:
		"""
		Exports a scenario to a certain directory.
		:param scenario: The scenario to export
		:param export_directory: The directory to export the scenario to.
		:return: None
		"""
		self.export_rendering(scenario=scenario, export_directory=export_directory)
		if scenario.trees is not None:
			exportable_trees = self.get_exportable_detections(
				detections=scenario.trees,
				tile_x_nw=scenario.request.x_grid_coord,
				tile_y_nw=scenario.request.y_grid_coord
			)
			exportable_trees["generated"] = exportable_trees["label"].apply(
				lambda str: 0 if str == "Tree" else 1
			)
			exportable_trees.to_csv(export_directory.joinpath("trees.csv"), index=False)
		if scenario.cars is not None:
			exportable_cars = self.get_exportable_detections(
				detections=scenario.cars,
				tile_x_nw=scenario.request.x_grid_coord,
				tile_y_nw=scenario.request.y_grid_coord
			)
			exportable_cars.to_csv(export_directory.joinpath("cars.csv"), index=False)
		if scenario.buildings is not None:
			exportable_buildings = RequestExporter.prepare_geodataframe(
				request=scenario.request, geo_dataframe=scenario.buildings
			)
			exportable_buildings.to_file(
				driver='GeoJSON', filename=str(export_directory.joinpath("buildings.geojson"))
			)
