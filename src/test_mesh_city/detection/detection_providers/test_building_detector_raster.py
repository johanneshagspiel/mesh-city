# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest
from math import ceil

import numpy as np
from scipy import stats
from pathlib import Path
from PIL import Image
from sklearn.feature_extraction.image import extract_patches_2d, reconstruct_from_patches_2d

from mesh_city.detection.detection_providers.building_detector import BuildingDetector
from mesh_city.util.file_handler import FileHandler
from sklearn.feature_extraction import image

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
		result_image = Image.fromarray(building_detector.detect(
			np.asarray(Image.open(Path(__file__).parents[0].joinpath("test-images/test1.png")).resize((512,512)))
		),'L')
		ground_truth = Image.open(
			Path(__file__).parents[0].joinpath("test-images/groundtruth1.png")
		).convert('L')
		print()
		self.assertGreaterEqual(compute_image_similarity(result_image, ground_truth), 0.9)

	def create_tile_dictionary(self, data, tile_width,tile_height):
		image_width = data.shape[0]
		image_height = data.shape[1]
		assert tile_width <= image_width
		assert tile_height <= image_height
		tile_dictionary = {}
		for x in range(ceil(image_width/tile_width)):
			for y in range(ceil(image_height / tile_height)):
				upper_y = min(image_height-tile_height,y*tile_height)
				left_x = min(image_width-tile_width,x*tile_width)
				tile_dictionary[(left_x,upper_y)] = data[upper_y:upper_y+tile_height,left_x:left_x+tile_width]
		return tile_dictionary

	def reconstruct_image_from_dict(self, tile_dictionary, tile_width, tile_height,image_width,image_height):
		array = np.empty((image_height,image_width))
		print(array)
		for (x,y) in tile_dictionary:
			print(array[y:y+tile_height,x:x+tile_width])
			print(tile_dictionary[(x,y)])
			array[y:y+tile_height,x:x+tile_width] = tile_dictionary[(x,y)]
		return array

	def test_dict(self):
		data = np.arange(16).reshape(4,4).astype(np.int8)
		dictionary = self.create_tile_dictionary(data, 2, 2)
		print(data)
		print(dictionary)
		print(self.reconstruct_image_from_dict(dictionary,2,2,4,4))

	def test(self):
		image = Image.open(Path(__file__).parents[0].joinpath("test-images/test1.png"))
		# for now a constant, can be used to tweak the number of pixels per square meter
		scaling_factor = 0.333333333333333333333333333333
		scaled_image = image.resize((int(image.width*scaling_factor),int(image.height*scaling_factor)))
		array = np.asarray(scaled_image)
		tile_dict = self.create_tile_dictionary(array,512,512)
		print(len(tile_dict))

		building_detector = BuildingDetector(FileHandler())
		for (x,y) in tile_dict:
			Image.fromarray(tile_dict[(x, y)], "RGB").show()
			tile_dict[(x,y)] = building_detector.detect(tile_dict[(x,y)])
			ImageUtil.greyscale_matrix_to_image(tile_dict[(x,y)]).show()
		result = self.reconstruct_image_from_dict(tile_dict,512,512,scaled_image.width,scaled_image.height)
		final_image = ImageUtil.greyscale_matrix_to_image(result)
		final_image.save(Path(__file__).parents[0].joinpath("test-images/tiledresult1.png"))
		# reconstruction = np.int8(reconstruct_from_patches_2d(patches, array.shape))
		# print(reconstruction)
		# np.testing.assert_array_almost_equal(array, reconstruction)

