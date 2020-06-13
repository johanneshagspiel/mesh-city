"""
A module containing the pipeline class which is responsible for moving images to the appropriate
detection algorithm in a form and frequency that they require and then moving the results to the
appropriate classes to create useful information in the form of overlays.
"""

from enum import Enum
from typing import List, Sequence

import geopandas
import numpy as np
import pandas as pd
from PIL import Image

from mesh_city.detection.detection_providers.building_detector import BuildingDetector
from mesh_city.detection.detection_providers.deep_forest import DeepForest
from mesh_city.detection.raster_vector_converter import RasterVectorConverter
from mesh_city.request.google_layer import GoogleLayer
from mesh_city.request.layer import Layer
from mesh_city.request.request import Request
from mesh_city.request.request_manager import RequestManager
from mesh_city.request.trees_layer import TreesLayer
from mesh_city.util.file_handler import FileHandler


class DetectionType(Enum):
	"""
	An enum defining the types of features that can be detected.
	"""
	TREES = 0
	BUILDINGS = 1
	CARS = 2


class Pipeline:
	"""
	A class responsible for moving data to the detection algorithm in a way they like and then
	routing the results to the appropriate classes to create useful information.
	"""

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
				tiles = request.get_layer_of_type(GoogleLayer).tiles
				deep_forest = DeepForest()
				tree_detections_path = self.request_manager.get_image_root().joinpath("trees")
				tree_detections_path.mkdir(parents=True, exist_ok=True)
				detection_file_path = tree_detections_path.joinpath(
					"detections_" + str(request.request_id) + ".csv"
				)
				frames = []
				for tile in tiles:
					x_offset = (tile.x_grid_coord - request.x_grid_coord) * 1024
					y_offset = (tile.y_grid_coord - request.y_grid_coord) * 1024
					image = Image.open(tile.path).convert("RGB")
					np_image = np.array(image)
					result = deep_forest.detect(np_image)
					result["xmin"] += x_offset
					result["ymin"] += y_offset
					result["xmax"] += x_offset
					result["ymax"] += y_offset
					frames.append(result)
				concat_result = pd.concat(frames).reset_index(drop=True)
				concat_result.to_csv(detection_file_path)
				new_layers.append(
					TreesLayer(
					width=request.num_of_horizontal_images,
					height=request.num_of_vertical_images,
					detections_path=detection_file_path
					)
				)
			if feature == DetectionType.BUILDINGS:
				tiles = request.get_layer_of_type(GoogleLayer).tiles
				building_detector = BuildingDetector(
					nn_weights_path=self.file_handler.folder_overview["resource_path"].
					joinpath("neural_networks/xdxd_spacenet4_solaris_weights.pth")
				)
				building_detections_path = self.request_manager.get_image_root(
				).joinpath("buildings")
				building_detections_path.mkdir(parents=True, exist_ok=True)
				detection_file_path = building_detections_path.joinpath(
					"detections_" + str(request.request_id) + ".csv"
				)

				for tile in tiles:
					x_offset = (tile.x_grid_coord - request.x_grid_coord) * 1024
					y_offset = (tile.y_grid_coord - request.y_grid_coord) * 1024
					image = Image.open(tile.path).convert("RGB").resize((512,512))
					np_image = np.array(image)
					raster_detections = building_detector.detect(image=np_image)
					r2v = RasterVectorConverter()
					polygons = r2v.mask_to_vector(image=raster_detections)
					gpd.GeoDataFrame(geometry=gpd.GeoSeries(env))
					# result = pd.DataFrame(columns = ["xmin","ymin","xmax","ymax","score","label"])
					# result["xmin"] += x_offset
					# result["ymin"] += y_offset
					# result["xmax"] += x_offset
					# result["ymax"] += y_offset
					# frames.append(result)
				# concat_result = pd.concat(frames).reset_index(drop=True)
				# concat_result.to_csv(detection_file_path)
				# new_layers.append(
				# 	TreesLayer(
				# 	width=request.num_of_horizontal_images,
				# 	height=request.num_of_vertical_images,
				# 	detections_path=detection_file_path
				# 	)
				# )

		return new_layers
