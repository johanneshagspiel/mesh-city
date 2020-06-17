# pylint: disable=C0114,R0201,W0703,missing-class-docstring,missing-function-docstring
import string
import unittest
from datetime import datetime

from mesh_city.user.image_provider_entity import ImageProviderEntity
from mesh_city.user.user_entity import UserEntity
from mesh_city.util.file_handler import FileHandler


class ImageProviderEntityTest(unittest.TestCase):

	def setUp(self):
		self.provider1 = ImageProviderEntity(
			FileHandler(),
			type_map_provider="Google Maps",
			api_key="AIzaSyD9cfAeQKFniipqRUgkcYy1sAtGXJYxNF4",
			quota=100,
			date_reset=datetime(2019, 2, 28)
		)
		self.provider2 = ImageProviderEntity(
			FileHandler(),
			type_map_provider="Mapbox",
			api_key="AIzaSyD9cfAeQKFniipqRUgkcYy1sAtGXJYxNF4",
			quota=100,
			date_reset=datetime(2019, 2, 28)
		)

	def test_serialize(self):
		provider_dict = {"ahn1": self.provider1, "ahn2": self.provider2}
		user_entity = UserEntity(FileHandler(), name="test user", image_providers=provider_dict)
		self.assertEqual(
			{
			'ahn1':
			{
			'api_key': 'AIzaSyD9cfAeQKFniipqRUgkcYy1sAtGXJYxNF4',
			'date_reset': '2020-06-30 00:00:00',
			'quota': 100,
			'type_map_provider': 'Google Maps',
			'usage': {
			'geocoding': 0, 'static_map': 0, 'total': 0
			}
			},
			'ahn2':
			{
			'api_key': 'AIzaSyD9cfAeQKFniipqRUgkcYy1sAtGXJYxNF4',
			'date_reset': '2020-06-30 00:00:00',
			'quota': 100,
			'type_map_provider': 'Mapbox',
			'usage': {
			'geocoding': 0, 'static_map': 0, 'total': 0
			}
			}
			},
			user_entity.for_storage()
		)
		print(user_entity.for_storage())

	def test_serialize_deserialize(self):
		test_json = {
			'test user':
			{
			'ahn1':
			{
			'type_map_provider': 'Google Maps',
			'api_key': 'AIzaSyD9cfAeQKFniipqRUgkcYy1sAtGXJYxNF4',
			'usage': {
			'static_map': 0, 'geocoding': 0, 'total': 0
			},
			'quota': 100.0,
			'date_reset': '2020-06-30'
			}
			}
		}
		remove = string.punctuation + string.whitespace

		test = UserEntity(FileHandler(), json=test_json)
		json_result = str(test.for_storage())
		temp_string = "{'test user': " + json_result + "}"

		to_compare_1 = str(test_json).translate(remove)
		to_compare_2 = temp_string.translate(remove)

		self.assertEqual(to_compare_1, to_compare_2)
