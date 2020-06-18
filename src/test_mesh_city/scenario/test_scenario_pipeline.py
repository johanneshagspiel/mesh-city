# pylint: disable=C0114,E1141,R0201,W0621,missing-class-docstring,missing-function-docstring

import unittest
from pathlib import Path

from mesh_city.request.request_manager import RequestManager
from mesh_city.scenario.scenario_pipeline import ScenarioModificationType, ScenarioPipeline
from mesh_city.util.file_handler import FileHandler


class TestScenarioPipeline(unittest.TestCase):

	def setUp(self) -> None:
		self.file_handler = FileHandler(root=Path(__file__).parents[1])
		self.request_manager = RequestManager(self.file_handler.folder_overview["image_path"])
		self.request_manager.load_data()

	def test_paint_buildings_scenario(self):
		pipeline = ScenarioPipeline(
			scenarios_to_create=[(ScenarioModificationType.PAINT_BUILDINGS_GREEN, 2)]
		)
		request = self.request_manager.get_request_by_id(0)
		scenario = pipeline.process(request)
		filtered_df = scenario.buildings.loc[scenario.buildings['label'] == "Shrubbery"]
		self.assertEqual(2,len(filtered_df))

	def test_swap_cars_scenario(self):
		pipeline = ScenarioPipeline(
			scenarios_to_create=[(ScenarioModificationType.SWAP_CARS, 3)]
		)
		request = self.request_manager.get_request_by_id(0)
		scenario = pipeline.process(request)
		filtered_df = scenario.trees.loc[scenario.trees['label'] == "SwappedCar"]
		self.assertEqual(3,len(filtered_df))

	def test_more_tree_scenario(self):
		pipeline = ScenarioPipeline(
			scenarios_to_create=[(ScenarioModificationType.MORE_TREES, 4)]
		)
		request = self.request_manager.get_request_by_id(0)
		scenario = pipeline.process(request)
		filtered_df = scenario.trees.loc[scenario.trees['label'] == "AddedTree"]
		self.assertEqual(4,len(filtered_df))
