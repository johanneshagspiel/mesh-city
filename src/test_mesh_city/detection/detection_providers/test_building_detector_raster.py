# pylint: disable=C0114,E1141,R0201,W0621,missing-class-docstring,missing-function-docstring

import unittest
from pathlib import Path

import numpy as np
from PIL import Image

from mesh_city.detection.detection_providers.building_detector import BuildingDetector
from mesh_city.detection.detection_providers.image_tiler import ImageTiler
from mesh_city.util.image_util import ImageUtil


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


class TestBuildingDetectorRaster(unittest.TestCase):

	def setUp(self):
		self.weights_path = Path(__file__).parents[2].joinpath(
			"resources", "neural_networks", "xdxd_spacenet4_solaris_weights.pth"
		)

	def test_building_detection(self):
		"""
		Fails if something goes wrong running a simple detection
		"""
		building_detector = BuildingDetector(nn_weights_path=self.weights_path)
		# TODO: Set up some type of test resource in the project structure to avoid things like this.
		result_image = ImageUtil.greyscale_matrix_to_image(
			building_detector.detect(
			np.asarray(
			Image.open(Path(__file__).parents[0].joinpath("test-images/test1.png")).resize((512, 512))
			)
			)
		)
		ground_truth = Image.open(
			Path(__file__).parents[0].joinpath("test-images/groundtruth1.png")
		).convert('L')
		self.assertGreaterEqual(compute_image_similarity(result_image, ground_truth), 0.9)

	def test_tiled_building_detection(self):
		image_tiler = ImageTiler(512, 512)
		image = Image.open(Path(__file__).parents[0].joinpath("test-images/test1.png")).resize(
			(1024, 1024)
		)
		array = np.asarray(image)
		tile_dict = image_tiler.create_tile_dictionary(array)

		building_detector = BuildingDetector(self.weights_path)
		for (x_coord, y_coord) in tile_dict:
			tile_dict[(x_coord, y_coord)] = building_detector.detect(tile_dict[(x_coord, y_coord)])
		result = image_tiler.construct_image_from_tiles(tile_dict)
		final_image = ImageUtil.greyscale_matrix_to_image(result).resize((512, 512))
		ground_truth = Image.open(
			Path(__file__).parents[0].joinpath("test-images/groundtruth1.png")
		).convert('L')
		self.assertGreaterEqual(compute_image_similarity(final_image, ground_truth), 0.85)
