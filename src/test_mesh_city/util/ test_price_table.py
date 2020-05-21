# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest

from parameterized import parameterized

from mesh_city.user.entities.image_provider_entity import ImageProviderEntity
from mesh_city.util.file_handler import FileHandler
from mesh_city.util.price_table_util import PriceTableUtil


class PriceTableTest(unittest.TestCase):

	def setUp(self):
		self.file_handler = FileHandler()

	@parameterized.expand(
		[
		["google_maps", "static_map", 0, 1, 100000,0.002],
		["google_maps", "static_map", 100000, 1, 1000000,0.002],
		["google_maps", "static_map", 100001, 1, 1000000,0.0016],
		["google_maps", "static_map", 500000, 1, 1000000,0.0016],
		["google_maps", "geocoding", 0, 1, 100000,0.005],
		["google_maps", "geocoding", 100000, 1, 1000000, 0.005],
		["google_maps", "geocoding", 100001, 1, 1000000, 0.004],
		["google_maps", "geocoding", 500000, 1, 1000000, 0.004],
		["mapbox", "static_map", 0, 1, 1000000, 0],
		["mapbox", "static_map", 50000, 1, 10000000,0],
		["mapbox", "static_map", 50001, 1, 10000000, 0.001],
		["mapbox", "static_map", 500000, 1, 10000000, 0.001],
		["mapbox", "static_map", 500001, 1, 10000000, 0.0008],
		["mapbox", "static_map", 1000000, 1, 10000000, 0.0008],
		["mapbox", "static_map", 1000001, 1, 10000000, 0.0006],
		["mapbox", "geocoding", 0, 1, 1000000, 0],
		["mapbox", "geocoding", 100000, 1, 10000000,0],
		["mapbox", "geocoding", 100001, 1, 10000000, 0.00075],
		["mapbox", "geocoding", 500000, 1, 10000000, 0.00075],
		["mapbox", "geocoding", 500001, 1, 10000000, 0.0006],
		["mapbox", "geocoding", 1000000, 1, 10000000, 0.0006],
		["mapbox", "geocoding", 1000001, 1, 10000000, 0.00045],
		]
	)
	def test_calculate_action_price(self, api_type, action_type, usage, requests, quota, price):
		self.assertEqual(
			PriceTableUtil.calculate_action_price(api_type, action_type, usage, requests, quota),
			price
		)

	def test_undefined_usage_range(self):
		self.assertRaises(ValueError, PriceTableUtil.calculate_action_price,"google_maps", "geocoding", 500001, 1, 1000000)

	def test_undefined_api(self):
		self.assertRaises(ValueError, PriceTableUtil.calculate_action_price,"map_map", "geocoding", 500001, 1, 1000000)

	def test_undefined_service(self):
		self.assertRaises(ValueError, PriceTableUtil.calculate_action_price,"google_maps", "undefined_test_service", 500001, 1, 1000000)
