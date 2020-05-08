# pylint: disable=C,R

import unittest

from mesh_city.main import print_start_info


class MainTestCase(unittest.TestCase):
	def test_main(self):
		print_start_info()
