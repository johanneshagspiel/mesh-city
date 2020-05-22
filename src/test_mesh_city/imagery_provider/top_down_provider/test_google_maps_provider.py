import requests
import unittest
from unittest import mock
from pathlib import Path

from PIL import Image

from mesh_city.imagery_provider.top_down_provider.google_maps_provider import GoogleMapsProvider
from mesh_city.user.quota_manager import QuotaManager
from mesh_city.user.user_info import UserInfo


class GoogleMapsProviderTest(unittest.TestCase):

	def setUp(self):
		self.user_info_init = UserInfo("Blue", "AIzaSyD9cfAeQKFniipqRUgkcYy1sAtGXJYxNF4"
		                               , 500, 25, 1452, 8, 15, 10, 55, 42)
		self.quota_manager_init = QuotaManager(self.user_info_init)
		# self.top_down_prov = TopDownProvider(self.user_info_init,self.quota_manager_init)
		self.google_maps_prov = GoogleMapsProvider(self.user_info_init, self.quota_manager_init)
		self.longitude = (11.999212921106265, 11.999195337295573)
		self.latitude = (12.000787078893735, 12.000804662704427)
		self.zoom = 2
		self.file_path = Path.joinpath(
			Path(__file__).parents[2], "resources"
		)

	def mock_response(self):
		mock_resp = mock.Mock()
		path = Path.joinpath(
			Path(__file__).parents[2], "resources", "test_response_image.png"
		)
		with open(path,"rb") as img:
			mock_resp.content = img.read()

		return mock_resp

	def test_get_and_store(self):
		g_map = self.google_maps_prov
		usage_before = self.user_info_init.usage
		g_map.get_and_store_location(latitude=self.latitude, longitude=self.longitude
		                             , zoom=self.zoom, filename="test_google_top_down.png"
		                             , new_folder_path=self.file_path
		                             , response=self.mock_response())
		self.assertEqual( (usage_before+1), self.user_info_init.usage)

