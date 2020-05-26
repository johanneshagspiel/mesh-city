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

	@staticmethod
	def matrix_to_image(matrix):
		image = Image.fromarray(np.array(object=matrix, dtype=np.uint8), 'RGB')
		return image

	def test_concat_horizontally(self):
		image_left = TestImageUtil.matrix_to_image(
			[[[255, 0, 0], [0, 255, 0]], [[0, 0, 255], [255, 255, 0]]]
		)
		image_right = TestImageUtil.matrix_to_image(
			[[[0, 255, 0], [0, 0, 255]], [[255, 0, 0], [0, 255, 255]]]
		)
		concatenated = ImageUtil.get_concat_horizontally(image_1=image_left, image_2=image_right)
		image_array = np.asarray(
			ImageUtil.get_concat_horizontally(image_1=image_left, image_2=image_right)
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
		image_left = TestImageUtil.matrix_to_image(
			[[[255, 0, 0], [0, 255, 0]], [[0, 0, 255], [255, 255, 0]]]
		)
		image_right = TestImageUtil.matrix_to_image(
			[[[0, 255, 0], [0, 0, 255]], [[255, 0, 0], [0, 255, 255]]]
		)
		image_array = np.asarray(
			ImageUtil.get_concat_vertically(image_1=image_left, image_2=image_right)
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
		test_image = TestImageUtil.matrix_to_image([[[255, 255, 255]]])
		result_array = np.asarray(ImageUtil.concat_image_grid(1, 1, [test_image]))
		target_array = np.asarray(test_image)
		self.assertEqual(result_array.shape, target_array.shape)
		self.assertEqual(result_array.all(), target_array.all())

	def test_2x2_grid(self):
		test_image_1 = TestImageUtil.matrix_to_image([[[255, 255, 255]]])
		test_image_2 = TestImageUtil.matrix_to_image([[[255, 255, 0]]])
		test_image_3 = TestImageUtil.matrix_to_image([[[255, 0, 255]]])
		test_image_4 = TestImageUtil.matrix_to_image([[[255, 0, 0]]])
		result_array = np.asarray(
			ImageUtil.concat_image_grid(
			2, 2, [test_image_1, test_image_2, test_image_3, test_image_4]
			)
		)
		target_array = np.array([[[255, 255, 255], [255, 255, 0]], [[255, 0, 255], [255, 0, 0]]])
		self.assertEqual(result_array.shape, target_array.shape)
		self.assertEqual(result_array.all(), target_array.all())

	def test_create_resized_copy(self):
		image = TestImageUtil.matrix_to_image(
			[[[255, 0, 0], [0, 255, 0]], [[0, 0, 255], [255, 255, 0]]]
		)
		image.save(str(Path(__file__).parents[0].joinpath("test.png")))
		img_util = ImageUtil()
		img_util.create_resized_copy(
			path_to_temp=Path(__file__).parents[0],
			width=4,
			height=4,
			path=Path(__file__).parents[0].joinpath("test.png"),
			name="large_test.png"
		)
		resized_image = Image.open(str(Path(__file__).parents[0].joinpath("large_test.png")))
		self.assertEqual(4, resized_image.width)
		self.assertEqual(4, resized_image.height)
		resized_image.close()

		# tears down the test
		os.remove(str(Path(__file__).parents[0].joinpath("large_test.png")))
		os.remove(str(Path(__file__).parents[0].joinpath("test.png")))
