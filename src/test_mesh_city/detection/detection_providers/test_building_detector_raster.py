# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest
from pathlib import Path

from PIL import Image

from mesh_city.detection.detection_providers.building_detector import BuildingDetector
from mesh_city.util.file_handler import FileHandler


def compute_image_similarity(image1, image2):
	assert image1.mode == image2.mode, "Different kinds of images."
	assert image1.size == image2.size, "Different sizes."

	pairs = zip(image1.getdata(), image2.getdata())
	if len(image1.getbands()) == 1:
		# for gray-scale jpegs
		dif = sum(abs(p1 - p2) for p1, p2 in pairs)
	else:
		dif = sum(abs(c1 - c2) for p1, p2 in pairs for c1, c2 in zip(p1, p2))

	ncomponents = image1.size[0] * image1.size[1] * 3
	return 1 - (dif / 255.0) / ncomponents


class BuildingDetectorRasterTest(unittest.TestCase):

	def test_construct_building_detector(self):
		"""
		Fails if weights file is not found or dependencies are not set up correctly
		"""
		BuildingDetector(FileHandler())

	def test_building_detection(self):
		"""
		Fails if something goes wrong running a simple detection
		"""
		building_detector = BuildingDetector(FileHandler())
		# TODO: Set up some type of test resource in the project structure to avoid things like this.
		result_image = building_detector.detect(
			Path(__file__).parents[0].joinpath("test-images/test1.png")
		)
		ground_truth = Image.open(
			Path(__file__).parents[0].joinpath("test-images/groundtruth1.png")
		).convert('L')
		print()
		self.assertGreaterEqual(compute_image_similarity(result_image, ground_truth), 0.9)
		# Uncomment for visual inspection of result
		# result_image.show()
