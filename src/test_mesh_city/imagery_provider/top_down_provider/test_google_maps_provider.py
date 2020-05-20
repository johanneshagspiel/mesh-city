import requests
import unittest
from unittest import mock
from pathlib import Path

from mesh_city.imagery_provider.top_down_provider.google_maps_provider import GoogleMapsProvider
from mesh_city.imagery_provider.top_down_provider.top_down_provider import TopDownProvider
from mesh_city.user.quota_manager import QuotaManager
from mesh_city.user.user_info import UserInfo


class GoogleMapsProviderTest(unittest.TestCase):

	def setUp(self):
		self.user_info_init = UserInfo("Blue", "a12ec", 500, 25, 1452, 8, 15, 10, 55, 42)
		self.quota_manager_init = QuotaManager(self.user_info_init)
		# self.top_down_prov = TopDownProvider(self.user_info_init,self.quota_manager_init)
		self.google_maps_prov = GoogleMapsProvider(self.user_info_init, self.quota_manager_init)
		self.longitude = (11.999212921106265, 11.999195337295573)
		self.latitude = (12.000787078893735, 12.000804662704427)
		self.zoom = 1
		self.file_path = Path.joinpath(
			Path(__file__).parents[1], "resources"
		)


	def test_get_and_store(self):
		g_map = self.google_maps_prov
		g_map.get_and_store_location(latitude=self.latitude, longitude=self.longitude
		                             , zoom=self.zoom, filename="test_google_top_down"
		                             , new_folder_path=self.file_path)
