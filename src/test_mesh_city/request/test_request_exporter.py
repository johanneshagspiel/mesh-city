import unittest
from pathlib import Path

from mesh_city.request.request import Request
from mesh_city.request.request_exporter import RequestExporter
from mesh_city.request.request_manager import RequestManager
from mesh_city.request.tile import Tile
from mesh_city.request.trees_layer import TreesLayer


class MyTestCase(unittest.TestCase):

	def setUp(self):
		self.path = Path("dummy_path")
		self.trees_layer = TreesLayer(
			width=1, height=1, detections_path=self.path
		)
		self.trees_layer.detections_export_path = self.path
		self.request = Request(
			request_id=42,
			x_grid_coord=0,
			y_grid_coord=0,
			num_of_horizontal_images=1,
			num_of_vertical_images=1,
			zoom=20,
			layers=[self.trees_layer]
		)

		self.request_manager = RequestManager(None)
		self.request_exporter = RequestExporter(self.request_manager)

	def test_get_export_csv(self):
		self.assertEqual(self.path, self.request_exporter.get_export_csv(self.request, self.trees_layer))
