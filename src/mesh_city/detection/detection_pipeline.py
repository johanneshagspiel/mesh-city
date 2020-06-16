"""
A module containing the pipeline class which is responsible for moving images to the appropriate
detection algorithm in a form and frequency that they require and then moving the results to the
appropriate classes to create useful information in the form of overlays.
"""

from enum import Enum
from typing import List, Sequence

import geopandas as gpd
import numpy as np
import pandas as pd
from PIL import Image

from mesh_city.detection.detection_providers.building_detector import BuildingDetector
from mesh_city.detection.detection_providers.car_detector import CarDetector
from mesh_city.detection.detection_providers.deep_forest import DeepForest
from mesh_city.detection.detection_providers.image_tiler import ImageTiler
from mesh_city.detection.raster_vector_converter import RasterVectorConverter
from mesh_city.request.entities.request import Request
from mesh_city.request.layers.buildings_layer import BuildingsLayer
from mesh_city.request.layers.cars_layer import CarsLayer
from mesh_city.request.layers.google_layer import GoogleLayer
from mesh_city.request.layers.layer import Layer
from mesh_city.request.layers.trees_layer import TreesLayer
from mesh_city.request.request_manager import RequestManager
from mesh_city.util.file_handler import FileHandler
from mesh_city.util.image_util import ImageUtil


class DetectionType(Enum):
	"""
	An enum defining the types of features that can be detected.
	"""
	TREES = 0
	BUILDINGS = 1
	CARS = 2


class DetectionPipeline:
	"""
	A class responsible for moving data to the detection algorithm in a way they like and then
	routing the results to the appropriate classes to create useful information.
	"""
	TILE_SIZE = 1024

	def __init__(
		self,
		file_handler: FileHandler,
		request_manager: RequestManager,
		detections_to_run: List[DetectionType]
	):
		"""
		The initialization method.

		:param application: the global application context
		:param detections_to_run: where to send the images to i.e. to detect trees
		:param main_screen: the main screen of the application
		"""
		self.file_handler = file_handler
		self.detections_to_run = detections_to_run
		self.request_manager = request_manager

	def detect_buildings(self, request: Request) -> BuildingsLayer:
		"""
		Detects buildings from a request's imagery.
		:param request: The request to detect buildings for.
		:return: A BuildingsLayer
		"""
		tiles = request.get_layer_of_type(GoogleLayer).tiles
		building_detector = BuildingDetector(
			nn_weights_path=self.file_handler.folder_overview["resource_path"].
			joinpath("neural_networks/xdxd_spacenet4_solaris_weights.pth")
		)
		building_detections_path = self.request_manager.get_image_root().joinpath("buildings")
		building_detections_path.mkdir(parents=True, exist_ok=True)
		detection_file_path = building_detections_path.joinpath(
			"detections_" + str(request.request_id) + ".geojson"
		)
		images = []
		for tile in tiles:
			images.append(Image.open(tile.path).convert("RGB").resize((512, 512), Image.ANTIALIAS))
		# note: not sure how this will perform for large scale analysis!
		concat = ImageUtil.concat_image_grid(
			request.num_of_horizontal_images, request.num_of_vertical_images, images
		)
		width, height = concat.size
		new_width, new_height = max(512, int(width / 6)), max(512, int(height / 6))
		small_concat = concat.resize((new_width, new_height), Image.ANTIALIAS)
		concat_image = np.asarray(small_concat)
		image_tiler = ImageTiler(tile_width=512, tile_height=512)
		patches = image_tiler.create_tile_dictionary(concat_image)
		mask_patches = {}
		for key in patches:
			mask_patches[key] = building_detector.detect(image=patches[key])
		concat_mask = np.uint8(image_tiler.construct_image_from_tiles(mask_patches))
		r2v = RasterVectorConverter()
		polygons = r2v.mask_to_vector(image=concat_mask)
		dataframe = gpd.GeoDataFrame(geometry=gpd.GeoSeries(polygons))
		dataframe.geometry = dataframe.geometry.scale(
			xfact=request.num_of_horizontal_images * 1024 / small_concat.width,
			yfact=request.num_of_vertical_images * 1024 / small_concat.height,
			zfact=1.0,
			origin=(0, 0)
		)
		dataframe.to_file(driver='GeoJSON', filename=detection_file_path)
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
		tiles = request.get_layer_of_type(GoogleLayer).tiles
		car_detector = CarDetector()
		tree_detections_path = self.request_manager.get_image_root().joinpath("cars")
		tree_detections_path.mkdir(parents=True, exist_ok=True)
		detections_path = tree_detections_path.joinpath(
			"detections_" + str(request.request_id) + ".csv"
		)
		frames = []

		for tile in tiles:
			x_offset = (tile.x_grid_coord - request.x_grid_coord) * DetectionPipeline.TILE_SIZE
			y_offset = (tile.y_grid_coord - request.y_grid_coord) * DetectionPipeline.TILE_SIZE
			np_image = np.asarray(Image.open(tile.path).convert("RGB"))
			image_np_expanded = np.expand_dims(np_image, axis=0)
			result = car_detector.detect_cars(image_np_expanded)
			result["xmin"] += x_offset
			result["ymin"] += y_offset
			result["xmax"] += x_offset
			result["ymax"] += y_offset
			frames.append(result)
		concat_result = pd.concat(frames).reset_index(drop=True)
		concat_result.to_csv(detections_path)
		return CarsLayer(
			width=request.num_of_horizontal_images,
			height=request.num_of_vertical_images,
			detections_path=detections_path
		)

	def detect_trees(self, request: Request) -> TreesLayer:
		"""
		Detects trees from a request's imagery.
		:param request: The request to detect trees for.
		:return: A TreesLayer
		"""
		tiles = request.get_layer_of_type(GoogleLayer).tiles
		deep_forest = DeepForest()
		tree_detections_path = self.request_manager.get_image_root().joinpath("trees")
		tree_detections_path.mkdir(parents=True, exist_ok=True)
		detection_file_path = tree_detections_path.joinpath(
			"detections_" + str(request.request_id) + ".csv"
		)
		images = []
		for tile in tiles:
			images.append(Image.open(tile.path).convert("RGB").resize((512, 512), Image.ANTIALIAS))
		# note: not sure how this will perform for large scale analysis!
		concat = ImageUtil.concat_image_grid(
			request.num_of_horizontal_images, request.num_of_vertical_images, images
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

		result.to_csv(detection_file_path)
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

		if not request.has_layer_of_type(GoogleLayer):
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
