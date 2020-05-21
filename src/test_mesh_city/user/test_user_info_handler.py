# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest
from pathlib import Path

from mesh_city.user.user_info import UserInfo
from mesh_city.user.user_info_handler import UserInfoHandler


class UserInfoHandlerTest(unittest.TestCase):

	def setUp(self):
		self.api_file_path = Path.joinpath(
			Path(__file__).parents[1], "resources", "test_api_key.json"
		)
		self.user_info_init = UserInfo("Blue", "a12ec", 500, 25, 1452, 8, 15, 10, 55, 42)
		self.user_handler = UserInfoHandler(self.api_file_path)
		self.user_handler.store_user_info(self.user_info_init)  # Needed for changing the file back.

	def alt_set_up(self):
		self.api_file_path = "/nowhereland/here"
		self.user_handler = UserInfoHandler(self.api_file_path)

	def test_load_user_info(self):
		info = self.user_handler.load_user_info()
		user_info = self.user_info_init
		self.assertEqual(info.__dict__, user_info.__dict__)

	def test_store_user_info(self):
		store_this = UserInfo("Green", "a12ec", 500, 25, 1452, 8, 15, 10, 55, 42)
		self.user_handler.store_user_info(store_this)
		# now have to load it again to read it
		stored_name = self.user_handler.load_user_info().name
		self.assertEqual(stored_name, "Green")

	def test_file_exists(self):
		flag = self.user_handler.file_exists()
		self.assertTrue(flag)

	def test_file_exists_not(self):
		self.alt_set_up()
		flag = self.user_handler.file_exists()
		self.assertFalse(flag)
