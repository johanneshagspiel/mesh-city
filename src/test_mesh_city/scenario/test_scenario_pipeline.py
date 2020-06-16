# pylint: disable=C0114,E1141,R0201,W0621,missing-class-docstring,missing-function-docstring

import unittest
from pathlib import Path

from mesh_city.request.request_manager import RequestManager
from mesh_city.request.scenario.scenario_pipeline import ScenarioPipeline, ScenarioType
from mesh_city.util.file_handler import FileHandler


class TestScenarioPipeline(unittest.TestCase):

	def test_more_tree_scenario(self):
		file_handler = FileHandler(root=Path(__file__).parents[1])
		request_manager = RequestManager(file_handler.folder_overview["image_path"])
		request_manager.load_data()
		pipeline = ScenarioPipeline(
			scenarios_to_create=[ScenarioType.MORE_TREES]
		)
		request = request_manager.get_request_by_id(0)
		pipeline.process(request)
