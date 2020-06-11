# pylint: disable=C0114,E1141,R0201,W0621,missing-class-docstring,missing-function-docstring

import unittest

from mesh_city.detection.pipeline import DetectionType, Pipeline
from mesh_city.request.request_manager import RequestManager
from mesh_city.util.file_handler import FileHandler


class TestPipeline(unittest.TestCase):

	def test_tiled_building_detection(self):
		file_handler = FileHandler()
		request_manager = RequestManager(file_handler.folder_overview["image_path"])
		request_manager.load_data()
		pipeline = Pipeline(request_manager, type_of_detection=[DetectionType.TREES])
		request = request_manager.get_request_by_id(0)
		pipeline.process(request)
