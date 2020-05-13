import unittest

from mesh_city.user.user_info_handler import UserInfoHandler


class MainTestCase(unittest.TestCase):
	""" An example test case for main """

	def test_main(self):
		""" A (useless) example test for the splash message """
		handler = UserInfoHandler()
		print(handler.load_user_info().__dict__)
