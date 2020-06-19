# pylint: disable=C0114,E1141,R0201,W0621,missing-class-docstring,missing-function-docstring

import unittest
from pathlib import Path

from PIL import Image

from mesh_city.request.request_manager import RequestManager
from mesh_city.scenario.scenario_exporter import ScenarioExporter
from mesh_city.scenario.scenario_pipeline import ScenarioModificationType, ScenarioPipeline
from mesh_city.util.file_handler import FileHandler


class TestScenarioExporter(unittest.TestCase):

	def setUp(self) -> None:
		self.file_handler = FileHandler(root=Path(__file__).parents[1])
		self.request_manager = RequestManager(self.file_handler.folder_overview["image_path"])
		self.request_manager.load_data()

	def test_get_tree_crops(self):
		pipeline = ScenarioPipeline(
			scenarios_to_create=[(ScenarioModificationType.PAINT_BUILDINGS_GREEN, 2)]
		)
		request = self.request_manager.get_request_by_id(0)
		scenario = pipeline.process(request)
		overlay_image = Image.open(
			self.file_handler.folder_overview["resource_path"].joinpath("test-overlay.png")
		).convert("RGB")
		exporter = ScenarioExporter(
			request_manager=self.request_manager, overlay_image=overlay_image
		)
		tree_crops = exporter.get_tree_crops(scenario=scenario)
		tree_crops[0].show()
		tree_crops[5].show()

	def test_replace_cars(self):
		pipeline = ScenarioPipeline(scenarios_to_create=[(ScenarioModificationType.SWAP_CARS, 2)])
		request = self.request_manager.get_request_by_id(0)
		scenario = pipeline.process(request)
		overlay_image = Image.open(
			self.file_handler.folder_overview["resource_path"].joinpath("test-overlay.png")
		).convert("RGB")
		exporter = ScenarioExporter(
			request_manager=self.request_manager, overlay_image=overlay_image
		)
		exporter.export_scenario(
			scenario=scenario, export_directory=self.file_handler.folder_overview["resource_path"]
		)

	def test_paint_buildings_scenario(self):
		pipeline = ScenarioPipeline(
			scenarios_to_create=[(ScenarioModificationType.PAINT_BUILDINGS_GREEN, 2)]
		)
		request = self.request_manager.get_request_by_id(0)
		scenario = pipeline.process(request)
		overlay_image = Image.open(
			self.file_handler.folder_overview["resource_path"].joinpath("test-overlay.png")
		).convert("RGB")
		exporter = ScenarioExporter(
			request_manager=self.request_manager, overlay_image=overlay_image
		)
		exporter.export_scenario(
			scenario=scenario, export_directory=self.file_handler.folder_overview["resource_path"]
		)
