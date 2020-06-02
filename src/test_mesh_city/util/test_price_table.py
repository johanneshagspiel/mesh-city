# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest

from parameterized import parameterized

from mesh_city.util.price_table_util import PriceTableUtil, QuotaException


class PriceTableTest(unittest.TestCase):

	def setUp(self):
		pass

	@parameterized.expand(
		[
		["Google Maps", "static_map", 0, 1, 100000,
		0.002], ["Google Maps", "static_map", 100000, 1, 1000000,
		0.002], ["Google Maps", "static_map", 100001, 1, 1000000,
		0.0016], ["Google Maps", "static_map", 500000, 1, 1000000,
		0.0016], ["Google Maps", "geocoding", 0, 1, 100000,
		0.005], ["Google Maps", "geocoding", 100000, 1, 1000000, 0.005],
		["Google Maps", "geocoding", 100001, 1, 1000000, 0.004], [
		"Google Maps", "geocoding", 500000, 1, 1000000, 0.004
		], ["Mapbox", "static_map", 0, 1, 1000000, 0], ["Mapbox", "static_map", 50000, 1, 10000000,
		0], ["Mapbox", "static_map", 50001, 1, 10000000, 0.001], [
		"Mapbox", "static_map", 500000, 1, 10000000, 0.001
		], ["Mapbox", "static_map", 500001, 1, 10000000, 0.0008], [
		"Mapbox", "static_map", 1000000, 1, 10000000, 0.0008
		], ["Mapbox", "static_map", 1000001, 1, 10000000, 0.0006],
		["Mapbox", "geocoding", 0, 1, 1000000, 0], ["Mapbox", "geocoding", 100000, 1, 10000000,
		0], ["Mapbox", "geocoding", 100001, 1, 10000000, 0.00075], [
		"Mapbox", "geocoding", 500000, 1, 10000000, 0.00075
		], ["Mapbox", "geocoding", 500001, 1, 10000000, 0.0006], [
		"Mapbox", "geocoding", 1000000, 1, 10000000, 0.0006
		], ["Mapbox", "geocoding", 1000001, 1, 10000000, 0.00045],
		]
	)
	def test_calculate_action_price(self, api_type, action_type, usage, requests, quota, price):
		self.assertEqual(
			PriceTableUtil.calculate_action_price(api_type, action_type, usage, requests, quota),
			price
		)

	def test_undefined_usage_range(self):
		self.assertRaises(
			ValueError,
			PriceTableUtil.calculate_action_price,
			"Google Maps",
			"geocoding",
			500001,
			1,
			1000000
		)

	def test_undefined_api(self):
		self.assertRaises(
			ValueError,
			PriceTableUtil.calculate_action_price,
			"map_map",
			"geocoding",
			500001,
			1,
			1000000
		)

	def test_undefined_service(self):
		self.assertRaises(
			ValueError,
			PriceTableUtil.calculate_action_price,
			"Google Maps",
			"undefined_test_service",
			500001,
			1,
			1000000
		)

	def test_exceed_quota(self):
		self.assertRaises(
			QuotaException,
			PriceTableUtil.calculate_action_price,
			"Google Maps",
			"geocoding",
			1000,
			1,
			1
		)
