# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring
import os
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

from mesh_city.util.image_util import ImageUtil


class TestImageUtil(unittest.TestCase):

	def setUp(self):
		pass

	def test_concat_grid(self):
		img_util = ImageUtil()
		test_images = [
			TestImageUtil.matrix_to_image([[[255, 255, 255], [255, 255, 255]]]),
			TestImageUtil.matrix_to_image([[[255, 255, 255], [255, 255, 0]]]),
			TestImageUtil.matrix_to_image([[[255, 255, 255], [255, 0, 255]]]),
			TestImageUtil.matrix_to_image([[[255, 255, 255], [255, 0, 0]]]),
			TestImageUtil.matrix_to_image([[[255, 255, 255], [0, 255, 255]]]),
			TestImageUtil.matrix_to_image([[[255, 255, 255], [0, 255, 255]]]),
			TestImageUtil.matrix_to_image([[[255, 255, 255], [0, 255, 0]]]),
			TestImageUtil.matrix_to_image([[[255, 255, 255], [0, 0, 255]]]),
			TestImageUtil.matrix_to_image([[[255, 255, 255], [0, 0, 0]]])
		]
		for index in range(1, 10):
			test_images[index -
				1].save(str(Path(__file__).parents[0]) + "/" + str(index) + "_test.png")

		target_array = np.array(
			[
			[
			[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 0], [255, 255, 255],
			[255, 0, 255]
			],
			[
			[255, 255, 255], [255, 0, 0], [255, 255, 255], [0, 255, 255], [255, 255, 255],
			[0, 255, 255]
			],
			[[255, 255, 255], [0, 255, 0], [255, 255, 255], [0, 0, 255], [255, 255, 255], [0, 0, 0]]
			]
		)

		img_util.concat_images(
			new_folder_path=Path(__file__).parents[0], request=0, tile_number="0_0"
		)
		result_path = str(Path(__file__).parents[0].joinpath("concat_image_request_0_tile_0_0.png"))
		result_image = np.asarray(Image.open(result_path))
		self.assertEqual(result_image.shape, target_array.shape)
		self.assertEqual(result_image.all(), target_array.all())

		for index in range(1, 10):
			test_images[index - 1].close()
			os.remove(str(Path(__file__).parents[0]) + "/" + str(index) + "_test.png")
		os.remove(result_path)

	@staticmethod
	def matrix_to_image(matrix):
		image = Image.fromarray(np.array(object=matrix, dtype=np.uint8), 'RGB')
		return image

	def test_concat_horizontally(self):
		img_util = ImageUtil()
		image_left = self.matrix_to_image(
			[[[255, 0, 0], [0, 255, 0]], [[0, 0, 255], [255, 255, 0]]]
		)
		image_right = self.matrix_to_image(
			[[[0, 255, 0], [0, 0, 255]], [[255, 0, 0], [0, 255, 255]]]
		)
		image_array = np.asarray(
			img_util.get_concat_horizontally(image_1=image_left, image_2=image_right)
		)
		target_array = np.array(
			[
			[[255, 0, 0], [0, 255, 0], [0, 255, 0], [0, 0, 255]],
			[[0, 0, 255], [255, 255, 0], [255, 0, 0], [0, 255, 255]]
			]
		)
		self.assertEqual(image_array.shape, target_array.shape)
		self.assertEqual(image_array.all(), target_array.all())

	def test_concat_vertically(self):
		img_util = ImageUtil()
		image_left = self.matrix_to_image(
			[[[255, 0, 0], [0, 255, 0]], [[0, 0, 255], [255, 255, 0]]]
		)
		image_right = self.matrix_to_image(
			[[[0, 255, 0], [0, 0, 255]], [[255, 0, 0], [0, 255, 255]]]
		)
		image_array = np.asarray(
			img_util.get_concat_vertically(image_1=image_left, image_2=image_right)
		)
		target_array = np.array(
			[
			[[255, 0, 0], [0, 255, 0]], [[0, 0, 255], [255, 255, 0]], [[0, 255, 0], [0, 0, 255]],
			[[255, 0, 0], [0, 255, 255]]
			]
		)
		self.assertEqual(image_array.shape, target_array.shape)
		self.assertEqual(image_array.all(), target_array.all())

	def test_1x1_grid(self):
		img_util = ImageUtil()
		test_image = TestImageUtil.matrix_to_image([[[255, 255, 255]]])
		result_array = np.asarray(img_util.concat_image_grid(1, 1, [test_image]))
		target_array = np.asarray(test_image)
		self.assertEqual(result_array.shape, target_array.shape)
		self.assertEqual(result_array.all(), target_array.all())

	def test_2x2_grid(self):
		img_util = ImageUtil()
		test_image_1 = TestImageUtil.matrix_to_image([[[255, 255, 255]]])
		test_image_2 = TestImageUtil.matrix_to_image([[[255, 255, 0]]])
		test_image_3 = TestImageUtil.matrix_to_image([[[255, 0, 255]]])
		test_image_4 = TestImageUtil.matrix_to_image([[[255, 0, 0]]])
		result_array = np.asarray(
			img_util.concat_image_grid(
			2, 2, [test_image_1, test_image_2, test_image_3, test_image_4]
			)
		)
		target_array = np.array([[[255, 255, 255], [255, 255, 0]], [[255, 0, 255], [255, 0, 0]]])
		self.assertEqual(result_array.shape, target_array.shape)
		self.assertEqual(result_array.all(), target_array.all())

	def test_3x3_grid(self):
		img_util = ImageUtil()
		test_images = [
			TestImageUtil.matrix_to_image([[[255, 255, 255], [255, 255, 255]]]),
			TestImageUtil.matrix_to_image([[[255, 255, 255], [255, 255, 0]]]),
			TestImageUtil.matrix_to_image([[[255, 255, 255], [255, 0, 255]]]),
			TestImageUtil.matrix_to_image([[[255, 255, 255], [255, 0, 0]]]),
			TestImageUtil.matrix_to_image([[[255, 255, 255], [0, 255, 255]]]),
			TestImageUtil.matrix_to_image([[[255, 255, 255], [0, 255, 255]]]),
			TestImageUtil.matrix_to_image([[[255, 255, 255], [0, 255, 0]]]),
			TestImageUtil.matrix_to_image([[[255, 255, 255], [0, 0, 255]]]),
			TestImageUtil.matrix_to_image([[[255, 255, 255], [0, 0, 0]]])
		]
		result_array = np.asarray(img_util.concat_image_grid(3, 3, test_images))
		target_array = np.array(
			[
			[
			[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 0], [255, 255, 255],
			[255, 0, 255]
			],
			[
			[255, 255, 255], [255, 0, 0], [255, 255, 255], [0, 255, 255], [255, 255, 255],
			[0, 255, 255]
			],
			[[255, 255, 255], [0, 255, 0], [255, 255, 255], [0, 0, 255], [255, 255, 255], [0, 0, 0]]
			]
		)
		self.assertEqual(result_array.shape, target_array.shape)
		self.assertEqual(result_array.all(), target_array.all())
