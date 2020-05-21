# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest

from parameterized import parameterized

from mesh_city.user.entities.image_provider_entity import ImageProviderEntity
from mesh_city.util.file_handler import FileHandler
from mesh_city.util.price_table_util import PriceTableUtil


class PriceTableTest(unittest.TestCase):

	def setUp(self):
		self.file_handler = FileHandler()

	@parameterized.expand([["mapbox", "static_map", 1,0, 0.002] ])
	def test_calculate_action_price_mapbox(self,api_type,action_type,requests,previous_usage,price):
		json = {
			"type" : api_type,
			"api_key": "test",
			"usage" : previous_usage,
			"quota": 0,
			"date_reset": "2090-05-31",
			}
		image_provider_entity = ImageProviderEntity(file_handler=self.file_handler,json=json)
		price_util = PriceTableUtil(image_provider_entity=image_provider_entity,
		               action=[(action_type, requests)])
		self.assertEqual(price_util.calculate_action_price(), price)
