# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest

from parameterized import parameterized

from mesh_city.user.entities.image_provider_entity import ImageProviderEntity
from mesh_city.user.entities.user_entity import UserEntity
from mesh_city.user.quota_manager import QuotaManager
from mesh_city.util.file_handler import FileHandler
from mesh_city.util.price_table_util import PriceTableUtil


class PriceTableTest(unittest.TestCase):

	def setUp(self):
		self.file_handler = FileHandler()

	@parameterized.expand([["foo", "a", "a", ], ["bar", "a", "b"], ["lee", "b", "b"], ])
	def test_calculate_action_price_mapbox(self, provider, action, info, price):
		PriceTableUtil(image_provider_entity=ImageProviderEntity(file_handler=self.file_handler),
		               action=action).calculate_action_price()
		# action = [("static_map", number_requests)]
		# temp_cost = PriceTableUtil(image_provider_entity=value,
		# 	action=action).calculate_action_price()
		self.assertEqual(calculate_action_price(provider, action, info), price)
