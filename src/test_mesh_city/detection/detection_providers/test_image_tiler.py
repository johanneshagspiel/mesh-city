# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest

import numpy as np

from mesh_city.detection.detection_providers.image_tiler import ImageTiler


class ImageTilerTest(unittest.TestCase):

	def test_dict(self):
		image_tiler = ImageTiler(2, 2)
		image = np.arange(16).reshape(4, 4).astype(np.int8)
		dictionary = image_tiler.create_tile_dictionary(image)
		reconstructed_image = image_tiler.construct_image_from_tiles(dictionary)
		np.testing.assert_array_equal(image, reconstructed_image)
