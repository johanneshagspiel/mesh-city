# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest
from pathlib import Path

from mesh_city.detection.raster_vector_converter import RasterVectorConverter


class RasterVectorConverterTest(unittest.TestCase):

	def test_building_detection(self):
		"""
		Fails if something goes wrong running a simple detection
		"""

		polygons = RasterVectorConverter.mask_to_vector(
			Path(__file__).parents[0].joinpath("test-images/groundtruth1.png")
		)
		self.assertEqual(len(polygons), 22)
