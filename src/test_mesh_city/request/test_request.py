# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest
from pathlib import Path

from mesh_city.request.google_layer import GoogleLayer
from mesh_city.request.request import Request
from mesh_city.request.tile import Tile
from mesh_city.request.trees_layer import TreesLayer


class TestRequest(unittest.TestCase):

	def test_has_layer_of_type(self):
		google_layer = GoogleLayer(width=1,height=1,tiles=[Tile(path=Path("dummy_path"), x_coord=0, y_coord=0)])
		request = Request(request_id=42, x_coord=0, y_coord=0, width=1, height=1, zoom=20,
		                  layers=[google_layer])
		self.assertTrue(request.has_layer_of_type(GoogleLayer))

	def test_has_no_layer_of_type(self):
		google_layer = GoogleLayer(width=1,height=1,tiles=[Tile(path=Path("dummy_path"), x_coord=0, y_coord=0)])
		request = Request(request_id=42, x_coord=0, y_coord=0, width=1, height=1, zoom=20,
		                  layers=[google_layer])
		with self.assertRaises(ValueError):
			request.get_layer_of_type(TreesLayer)
