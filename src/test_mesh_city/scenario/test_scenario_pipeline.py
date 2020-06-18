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
			request_manager=self.request_manager,
			scenarios_to_create=[(ScenarioModificationType.PAINT_BUILDINGS_GREEN, 2)],
			overlay_path=FileHandler().folder_overview["resource_path"].joinpath(
				"trees-overlay.png")
		)
		request = self.request_manager.get_request_by_id(0)
		pipeline.process(request)

	def test_swap_cars_scenario(self):
		pipeline = ScenarioPipeline(
			request_manager=self.request_manager,
			scenarios_to_create=[(ScenarioModificationType.SWAP_CARS, 3)],
			overlay_path=FileHandler().folder_overview["resource_path"].joinpath(
				"trees-overlay.png")
		)
		request = self.request_manager.get_request_by_id(0)
		pipeline.process(request)

	def test_more_tree_scenario(self):
		pipeline = ScenarioPipeline(
			request_manager=self.request_manager,
			scenarios_to_create=[(ScenarioModificationType.MORE_TREES, 4)],
			overlay_path=FileHandler().folder_overview["resource_path"].joinpath(
				"trees-overlay.png")
		)
		request = self.request_manager.get_request_by_id(0)
		pipeline.process(request)
