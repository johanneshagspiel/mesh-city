# pylint: disable=C0114,E1141,R0201,W0621,missing-class-docstring,missing-function-docstring

import unittest
from pathlib import Path

import geopandas as gpd
import pandas as pd

from mesh_city.detection.detection_pipeline import DetectionPipeline, DetectionType
from mesh_city.request.layers.buildings_layer import BuildingsLayer
from mesh_city.request.layers.cars_layer import CarsLayer
from mesh_city.request.layers.trees_layer import TreesLayer
from mesh_city.request.request_manager import RequestManager
from mesh_city.util.file_handler import FileHandler


class TestPipeline(unittest.TestCase):

	def setUp(self) -> None:
		self.file_handler = FileHandler(root=Path(__file__).parents[1])
		self.request_manager = RequestManager(self.file_handler.folder_overview["image_path"])
		self.request_manager.load_data()

	def test_tree_detection(self):
		pipeline = DetectionPipeline(
			FileHandler(), self.request_manager, detections_to_run=[DetectionType.TREES]
		)
		request = self.request_manager.get_request_by_id(0)
		pipeline.process(request)
		tree_dataframe = pd.read_csv(request.get_layer_of_type(TreesLayer).detections_path)
		self.assertGreaterEqual(len(tree_dataframe), 10)

	def test_car_detection(self):
		pipeline = DetectionPipeline(
			self.file_handler, self.request_manager, detections_to_run=[DetectionType.CARS]
		)
		request = self.request_manager.get_request_by_id(0)
		pipeline.process(request)
		car_dataframe = pd.read_csv(request.get_layer_of_type(CarsLayer).detections_path)
		self.assertGreaterEqual(len(car_dataframe), 3)

	def test_building_detection(self):
		pipeline = DetectionPipeline(
			self.file_handler, self.request_manager, detections_to_run=[DetectionType.BUILDINGS]
		)
		request = self.request_manager.get_request_by_id(0)
		pipeline.process(request)
		buildings_geodf = gpd.read_file(request.get_layer_of_type(BuildingsLayer).detections_path)
		self.assertTrue(len(buildings_geodf) < 20 and len(buildings_geodf) > 3)
