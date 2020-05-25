# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest

from mesh_city.util.geo_location_util import GeoLocationUtil


class TestImageUtil(unittest.TestCase):

	def setUp(self):

	def test_calc_meters_per_px(self):
		for zoom in range(23):
			answer_resolution = self.ground_resolutions[zoom]
			calculated_resolution = self.geo_location_util.calc_meters_per_px(0, zoom)
			self.assertAlmostEqual(answer_resolution, calculated_resolution, 4)

	def test_calc_next_location_latitude_true(self):
		answer_latitude = 51.91803031195189
		calculated_latitude = self.geo_location_util.calc_next_location_latitude(
			51.917534, 20, 600, True
		)
		self.assertEqual(answer_latitude, calculated_latitude)

	def test_calc_next_location_latitude_false(self):
		answer_latitude = 51.91703768804812
		calculated_latitude = self.geo_location_util.calc_next_location_latitude(
			51.917534, 20, 600, False
		)
		self.assertEqual(answer_latitude, calculated_latitude)

	def test_calc_next_location_longitude_true(self):
		answer_longitude = 4.456396662704557
		calculated_latitude = self.geo_location_util.calc_next_location_longitude(
			51.917534, 4.455592, 20, 600, True
		)
		self.assertEqual(answer_longitude, calculated_latitude)

	def test_calc_next_location_longitude_false(self):
		answer_longitude = 4.454787337295444
		calculated_latitude = self.geo_location_util.calc_next_location_longitude(
			51.917534, 4.455592, 20, 600, False
		)
		self.assertEqual(answer_longitude, calculated_latitude)
