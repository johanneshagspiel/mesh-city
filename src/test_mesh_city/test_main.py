# pylint: disable=C0114,R0201

import unittest

from mesh_city.main import print_start_info


class MainTestCase(unittest.TestCase):
	""" An example test case for main """

	def test_main(self):
		""" A (useless) example test for the splash message """
		print_start_info()
