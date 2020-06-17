# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest
from pathlib import Path

from mesh_city.request.entities.request import Request
from mesh_city.request.entities.tile import Tile
from mesh_city.request.layers.google_layer import GoogleLayer
from mesh_city.request.layers.trees_layer import TreesLayer


class TestRequest(unittest.TestCase):

	def test_has_layer_of_type(self):
		google_layer = GoogleLayer(
			width=1, height=1, tiles=[Tile(path=Path("dummy_path"), x_grid_coord=0, y_grid_coord=0)]
		)
		request = Request(
			request_id=42,
			x_grid_coord=0,
			y_grid_coord=0,
			num_of_horizontal_images=1,
			num_of_vertical_images=1,
			zoom=20,
			layers=[google_layer],
			name="test"
		)
		self.assertTrue(request.has_layer_of_type(GoogleLayer))

	def test_has_no_layer_of_type(self):
		google_layer = GoogleLayer(
			width=1, height=1, tiles=[Tile(path=Path("dummy_path"), x_grid_coord=0, y_grid_coord=0)]
		)
		request = Request(
			request_id=42,
			x_grid_coord=0,
			y_grid_coord=0,
			num_of_horizontal_images=1,
			num_of_vertical_images=1,
			zoom=20,
			layers=[google_layer],
			name="test"
		)
		with self.assertRaises(ValueError):
			request.get_layer_of_type(TreesLayer)
