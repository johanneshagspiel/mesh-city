# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest
from pathlib import Path

from mesh_city.request.entities.request import Request
from mesh_city.request.layers.trees_layer import TreesLayer
from mesh_city.request.request_exporter import RequestExporter
from mesh_city.request.request_manager import RequestManager
from mesh_city.util.file_handler import FileHandler


class RequestExporterTest(unittest.TestCase):

	def setUp(self):
		self.image_root = FileHandler(root=Path(__file__).parents[1]).folder_overview["image_path"]
		self.path = self.image_root.joinpath("trees", "detections_0.csv")
		self.trees_layer = TreesLayer(width=1, height=1, detections_path=self.path)
		self.trees_layer.detections_export_path = self.path
		self.request = Request(
			request_id=0,
			x_grid_coord=0,
			y_grid_coord=0,
			num_of_horizontal_images=1,
			num_of_vertical_images=1,
			zoom=20,
			layers=[self.trees_layer],
			name="test"
		)
		self.request_manager = RequestManager(image_root=self.image_root)
		self.request_exporter = RequestExporter(self.request_manager)

	def test_get_export_csv(self):
		self.assertEqual(
			self.image_root.joinpath("trees", "detections_0_export.csv"),
			self.request_exporter.get_export_csv(self.request, self.trees_layer)
		)
