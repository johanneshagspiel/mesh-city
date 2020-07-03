"""
A module containing the pipeline class which is responsible for moving images to the appropriate
detection algorithm in a form and frequency that they require and then moving the results to the
appropriate classes to create useful information in the form of overlays.
"""
import json
import time
from enum import Enum
from math import ceil, floor
from typing import Sequence

import geopandas as gpd
import numpy as np
import pandas as pd
from PIL import Image

from mesh_city.detection.detection_providers.building_detector import BuildingDetector
from mesh_city.detection.detection_providers.car_detector import CarDetector
from mesh_city.detection.detection_providers.image_tiler import ImageTiler
from mesh_city.detection.detection_providers.tree_detector import TreeDetector
from mesh_city.detection.raster_vector_converter import RasterVectorConverter
from mesh_city.request.entities.request import Request
from mesh_city.request.layers.buildings_layer import BuildingsLayer
from mesh_city.request.layers.cars_layer import CarsLayer
from mesh_city.request.layers.image_layer import ImageLayer
from mesh_city.request.layers.layer import Layer
from mesh_city.request.layers.trees_layer import TreesLayer
from mesh_city.request.request_manager import RequestManager
from mesh_city.util.file_handler import FileHandler
from mesh_city.util.image_util import ImageUtil
from mesh_city.util.observable import Observable


class DetectionType(Enum):
	"""
	An enum defining the types of features that can be detected.
	"""
	TREES = 0
	BUILDINGS = 1
	CARS = 2


class DetectionPipeline(Observable):
	"""
	A class responsible for moving data to the detection algorithm in a way they like and then
	routing the results to the appropriate classes to create useful information.
	"""
	TILE_SIZE = 1024

	def __init__(
		self,
		file_handler: FileHandler,
		request_manager: RequestManager,
		detections_to_run: Sequence[DetectionType]
	):
		"""
		The initialization method.

		:param application: the global application context
		:param detections_to_run: where to send the images to i.e. to detect trees
		:param main_screen: the main screen of the application
		"""
		super().__init__()
		self.file_handler = file_handler
		self.detections_to_run = detections_to_run
		self.request_manager = request_manager

	def detect_buildings(self, request: Request) -> BuildingsLayer:
		"""
		Detects buildings from a request's imagery.
		:param request: The request to detect buildings for.
		:return: A BuildingsLayer
		"""
		tiles = request.get_layer_of_type(ImageLayer).tiles
		building_detector = BuildingDetector(
			nn_weights_path=self.file_handler.folder_overview["resource_path"].
			joinpath("neural_networks/xdxd_spacenet4_solaris_weights.pth")
		)
		building_detections_path = self.request_manager.get_image_root().joinpath("buildings")
		building_detections_path.mkdir(parents=True, exist_ok=True)
		detection_file_path = building_detections_path.joinpath(
			"detections_" + str(request.request_id) + ".geojson"
		)
		cuts = self.compute_cuts(request)

		self.observable_state["detection_type"] = "Buildings"
		self.observable_state["total_tiles"] = len(cuts)
		self.observable_state["current_tile"] = 1
		self.observable_state["current_time_detection"] = 0
		self.notify_observers()
		frames = []
		for (counter, (cut_x,cut_y,cut_width,cut_height)) in enumerate(cuts, 1):
			start_time_download = time.time()
			x_offset = (cut_x-request.x_grid_coord) * DetectionPipeline.TILE_SIZE
			y_offset = (cut_y-request.y_grid_coord) * DetectionPipeline.TILE_SIZE
			images = []
			for tile in tiles:
				if tile.x_grid_coord>=cut_x and tile.x_grid_coord<cut_x+cut_width and tile.y_grid_coord>=cut_y and tile.y_grid_coord<cut_y+cut_height:
					images.append(
						Image.open(tile.path).convert("RGB").resize((512, 512), Image.ANTIALIAS))
			# note: not sure how this will perform for large scale analysis!
			concat = ImageUtil.concat_image_grid(
				cut_width, cut_height, images
			)
			width, height = concat.size
			new_width, new_height = max(512, int(width / 6)), max(512, int(height / 6))
			small_concat = concat.resize((new_width, new_height), Image.ANTIALIAS)
			concat_image = np.asarray(small_concat)
			image_tiler = ImageTiler(tile_width=512, tile_height=512)
			patches = image_tiler.create_tile_dictionary(concat_image)
			mask_patches = {}

			for key in patches:
				start_time_download = time.time()
				mask_patches[key] = building_detector.detect(image=patches[key])

			concat_mask = np.uint8(image_tiler.construct_image_from_tiles(mask_patches))
			r2v = RasterVectorConverter()
			polygons = r2v.mask_to_vector(image=concat_mask)
			dataframe = gpd.GeoDataFrame(geometry=gpd.GeoSeries(polygons))
			dataframe.geometry = dataframe.geometry.scale(
				xfact=cut_width * 1024 / small_concat.width,
				yfact=cut_height * 1024 / small_concat.height,
				zfact=1.0,
				origin=(0, 0)
			)
			dataframe.geometry = dataframe.geometry.translate(xoff=x_offset,yoff=y_offset,zoff=0)
			frames.append(dataframe)
			time_needed_download = time.time() - start_time_download
			self.observable_state["current_tile"] = counter
			self.observable_state["current_time_detection"] = time_needed_download
			self.notify_observers()

		concat_dataframe = pd.concat(frames).reset_index(drop=True)
		if not concat_dataframe.empty:
			concat_dataframe["label"] = "Building"
			concat_dataframe.to_file(driver='GeoJSON', filename=detection_file_path)
		else:
			empty_geojson = {"type": "FeatureCollection", "features": []}
			with open(detection_file_path, 'w') as json_file:
				json.dump(empty_geojson, json_file)
		return BuildingsLayer(
			width=request.num_of_horizontal_images,
			height=request.num_of_vertical_images,
			detections_path=detection_file_path
		)

	def detect_cars(self, request: Request) -> CarsLayer:
		"""
		Detects cars from a request's imagery.
		:param request: The request to detect cars for.
		:return: A CarsLayer
		"""
		tiles = request.get_layer_of_type(ImageLayer).tiles
		nn_weights_path = self.file_handler.folder_overview["resource_path"].joinpath(
			"neural_networks", "car_inference_graph.pb"
		)
		car_detector = CarDetector(nn_weights_path=nn_weights_path)
		tree_detections_path = self.request_manager.get_image_root().joinpath("cars")
		tree_detections_path.mkdir(parents=True, exist_ok=True)
		detections_path = tree_detections_path.joinpath(
			"detections_" + str(request.request_id) + ".csv"
		)
		frames = []

		self.observable_state["detection_type"] = "Cars"
		self.observable_state["total_tiles"] = len(tiles)
		self.observable_state["current_tile"] = 1
		self.observable_state["current_time_detection"] = 0
		self.notify_observers()

		for counter, tile in enumerate(tiles, 1):
			start_time_download = time.time()

			x_offset = (tile.x_grid_coord - request.x_grid_coord) * DetectionPipeline.TILE_SIZE
			y_offset = (tile.y_grid_coord - request.y_grid_coord) * DetectionPipeline.TILE_SIZE
			np_image = np.asarray(Image.open(tile.path).convert("RGB").resize((256, 256)))
			image_np_expanded = np.expand_dims(np_image, axis=0)
			result = car_detector.detect_cars(image_np_expanded)
			result["xmin"] += x_offset
			result["ymin"] += y_offset
			result["xmax"] += x_offset
			result["ymax"] += y_offset
			frames.append(result)

			time_needed_download = time.time() - start_time_download
			self.observable_state["current_tile"] = counter
			self.observable_state["current_time_detection"] = time_needed_download
			self.notify_observers()
		car_detector.close()
		concat_result = pd.concat(frames).reset_index(drop=True)
		concat_result.to_csv(detections_path)

		return CarsLayer(
			width=request.num_of_horizontal_images,
			height=request.num_of_vertical_images,
			detections_path=detections_path
		)

	def compute_cuts(self, request: Request):
		max_subgrid_dimension = 16
		num_vertical_cuts = ceil(request.num_of_vertical_images/max_subgrid_dimension)
		num_horizontal_cuts = ceil(request.num_of_horizontal_images/max_subgrid_dimension)
		cuts = []
		for vertical_cut in range(num_vertical_cuts):
			vertical_cut_size = max_subgrid_dimension
			cut_y = vertical_cut_size * vertical_cut
			if vertical_cut == num_vertical_cuts - 1:
				vertical_cut_size = request.num_of_vertical_images - vertical_cut*max_subgrid_dimension
			for horizontal_cut in range(num_horizontal_cuts):
				horizontal_cut_size = max_subgrid_dimension
				cut_x = horizontal_cut_size * horizontal_cut
				if horizontal_cut == num_horizontal_cuts - 1:
					horizontal_cut_size = request.num_of_horizontal_images - horizontal_cut * max_subgrid_dimension
				cuts.append((cut_x+request.x_grid_coord,cut_y+request.y_grid_coord,horizontal_cut_size,vertical_cut_size))
		return cuts

	def detect_trees(self, request: Request) -> TreesLayer:
		"""
		Detects trees from a request's imagery.
		:param request: The request to detect trees for.
		:return: A TreesLayer
		"""
		tiles = request.get_layer_of_type(ImageLayer).tiles
		nn_weights_path = self.file_handler.folder_overview["resource_path"].joinpath(
			"neural_networks", "NEON.h5"
		)
		deep_forest = TreeDetector(nn_weights_path=nn_weights_path)
		tree_detections_path = self.request_manager.get_image_root().joinpath("trees")
		tree_detections_path.mkdir(parents=True, exist_ok=True)
		detection_file_path = tree_detections_path.joinpath(
			"detections_" + str(request.request_id) + ".csv"
		)
		frames = []
		cuts = self.compute_cuts(request)
		self.observable_state["detection_type"] = "Trees"
		self.observable_state["total_tiles"] = len(cuts)
		self.observable_state["current_tile"] = 1
		self.observable_state["current_time_detection"] = 0
		self.notify_observers()
		for (counter, (cut_x,cut_y,cut_width,cut_height)) in enumerate(cuts, 1):
			start_time_download = time.time()

			x_offset = (cut_x-request.x_grid_coord) * DetectionPipeline.TILE_SIZE
			y_offset = (cut_y-request.y_grid_coord) * DetectionPipeline.TILE_SIZE

			images = []
			for tile in tiles:
				if tile.x_grid_coord>=cut_x and tile.x_grid_coord<cut_x+cut_width and tile.y_grid_coord>=cut_y and tile.y_grid_coord<cut_y+cut_height:
					images.append(
						Image.open(tile.path).convert("RGB").resize((512, 512), Image.ANTIALIAS))
			# note: not sure how this will perform for large scale analysis!
			concat = ImageUtil.concat_image_grid(
				cut_width, cut_height, images
			)
			width, height = concat.size
			small_concat = concat.resize((int(width / 3), int(height / 3)), Image.ANTIALIAS)
			concat_scratch_path = tree_detections_path.joinpath(
				"temp_" + str(request.request_id) + ".png"
			)
			small_concat.save(concat_scratch_path)
			result = deep_forest.detect(path=concat_scratch_path)
			concat_scratch_path.unlink()
			result["xmin"] = result["xmin"] * 6
			result["ymin"] = result["ymin"] * 6
			result["xmax"] = result["xmax"] * 6
			result["ymax"] = result["ymax"] * 6
			result["xmin"] += x_offset
			result["ymin"] += y_offset
			result["xmax"] += x_offset
			result["ymax"] += y_offset
			frames.append(result)

			time_needed_download = time.time() - start_time_download
			self.observable_state["current_tile"] = counter
			self.observable_state["current_time_detection"] = time_needed_download
			self.notify_observers()
		concat_result = pd.concat(frames).reset_index(drop=True)
		concat_result.to_csv(detection_file_path)

		return TreesLayer(
			width=request.num_of_horizontal_images,
			height=request.num_of_vertical_images,
			detections_path=detection_file_path
		)

	def process(self, request: Request) -> Sequence[Layer]:
		"""
		Processes a request that is assumed to have a GoogleLayer with imagery (errors otherwise) and
		returns a list of detection layers corresponding to the detections_to_run variable.

		:param request: The request to process. Must have a GoogleLayer
		:return:
		"""

		if not request.has_layer_of_type(ImageLayer):
			raise ValueError("The request to process should have imagery to detect features from")

		new_layers = []
		for feature in self.detections_to_run:
			if feature == DetectionType.TREES:
				new_layers.append(self.detect_trees(request=request))
			if feature == DetectionType.BUILDINGS:
				new_layers.append(self.detect_buildings(request=request))
			if feature == DetectionType.CARS:
				new_layers.append(self.detect_cars(request=request))
		return new_layers
