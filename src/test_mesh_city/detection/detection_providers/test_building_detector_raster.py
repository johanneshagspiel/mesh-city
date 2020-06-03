# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest

from mesh_city.detection.detection_providers.building_detector import BuildingDetector
from mesh_city.util.file_handler import FileHandler


class BuildingDetectorRasterTest(unittest.TestCase):

	def test_construct_building_detector(self):
		"""
		Fails if weights file is not found or dependencies are not set up correctly
		"""
		BuildingDetector(FileHandler())
