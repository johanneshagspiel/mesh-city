# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest

from mesh_city.util.geo_location_util import GeoLocationUtil


class TestGeoLocationUtil(unittest.TestCase):

	def setUp(self):
		self.geo_location_util = GeoLocationUtil()
		# correct ground resolutions (meters per pixel) at the Equator for zoom levels 0 to 23
		# level 0 being 156543.03392
		self.ground_resolutions = [
			156543.03392,
			78271.5170,
			39135.7585,
			19567.8792,
			9783.9396,
			4891.9698,
			2445.9849,
			1222.9925,
			611.4962,
			305.7481,
			152.8741,
			76.4370,
			38.2185,
			19.1093,
			9.5546,
			4.7773,
			2.3887,
			1.1943,
			0.5972,
			0.2986,
			0.1493,
			0.0746,
			0.0373,
			0.0187
		]

	def test_calc_meters_per_px(self):
		for zoom in range(23):
			answer_resolution = self.ground_resolutions[zoom]
			calculated_resolution = self.geo_location_util.calc_meters_per_px(0, zoom)
			self.assertAlmostEqual(answer_resolution, calculated_resolution, 4)

	# /def test_calc_next_location_latitude(self):
