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
		[0, 0, -99999]]
		]
	)
	def test_calculate_action_price(self, api_type, action_type, usage, requests, quota, price):
		self.assertEqual(
			PriceTableUtil.calculate_action_price(api_type, action_type, usage, requests, quota),
			price
		)

	def test_undefined_usage_range(self):
		self.assertEqual(
			[-1, 0.995, 198, -999999.995],
			PriceTableUtil.calculate_action_price(
			"Google Maps",
			"geocoding",
			500001,
			1,
			1000000)
		)

	def test_undefined_api(self):
		self.assertEqual(
			[-1, 0.995, 198, -999999.995],
			PriceTableUtil.calculate_action_price(
			"Google Maps",
			"geocoding",
			500001,
			1,
			1000000)
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
		self.assertEqual(
			[-1, 0.995, 198, -0.9950000000000008],
			PriceTableUtil.calculate_action_price(
			"Google Maps",
			"geocoding",
			1000,
			1,
			1)
		)
