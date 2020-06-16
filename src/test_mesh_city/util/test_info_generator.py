# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring
import os
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

from mesh_city.util.image_util import ImageUtil


class TestInfoGenerator(unittest.TestCase):

	def setUp(self):
		pass

	def test_get_tree_co2_values(self):
		self.InfoGenera
