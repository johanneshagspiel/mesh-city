# pylint: disable=C0114,E1141,R0201,W0621,missing-class-docstring,missing-function-docstring

import unittest
from pathlib import Path

from mesh_city.detection.detection_pipeline import DetectionPipeline, DetectionType
from mesh_city.request.request_manager import RequestManager
from mesh_city.util.file_handler import FileHandler


class TestPipeline(unittest.TestCase):

	def test_tree_detection(self):
		file_handler = FileHandler()
		request_manager = RequestManager(file_handler.folder_overview["image_path"])
		request_manager.load_data()
		pipeline = DetectionPipeline(
			FileHandler(), request_manager, detections_to_run=[DetectionType.TREES]
		)
		request = request_manager.get_request_by_id(0)
		pipeline.process(request)

	def test_building_detection(self):
		file_handler = FileHandler(root=Path(__file__).parents[1])
		request_manager = RequestManager(file_handler.folder_overview["image_path"])
		request_manager.load_data()
		pipeline = DetectionPipeline(
			file_handler, request_manager, detections_to_run=[DetectionType.BUILDINGS]
		)
		request = request_manager.get_request_by_id(0)
		pipeline.process(request)
