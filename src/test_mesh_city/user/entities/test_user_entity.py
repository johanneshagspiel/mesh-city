# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest
from datetime import datetime

from mesh_city.user.entities.image_provider_entity import ImageProviderEntity
from mesh_city.user.entities.user_entity import UserEntity
from mesh_city.util.file_handler import FileHandler


class ImageProviderEntityTest(unittest.TestCase):

	def setUp(self):
		self.provider1 = ImageProviderEntity(
			FileHandler(),
			type_map_provider="google_maps",
			api_key="test",
			quota=100,
			usage=None,
			date_reset=datetime(2019, 2, 28)
		)
		self.provider2 = ImageProviderEntity(
			FileHandler(),
			type_map_provider="ahn",
			api_key="test",
			quota=100,
			usage=None,
			date_reset=datetime(2019, 2, 28)
		)

	def test_serialize(self):
		provider_dict = {"ahn1": self.provider1, "ahn2": self.provider2}
		user_entity = UserEntity(FileHandler(), name="test user", image_providers=provider_dict)
		self.assertEqual(
			{
			'test user':
			{
			'ahn1':
			{
			'api_key': 'test',
			'date_reset': '2020-05-31',
			'quota': 100,
			'type_map_provider': 'google_maps',
			'usage': {
			'geocoding': 0, 'static_map': 0, 'total': 0
			}
			},
			'ahn2':
			{
			'api_key': 'test',
			'date_reset': '2020-05-31',
			'quota': 100,
			'type_map_provider': 'ahn',
			'usage': {
			'geocoding': 0, 'static_map': 0, 'total': 0
			}
			}
			}
			},
			user_entity.for_json()
		)
		print(user_entity.for_json())

	def test_serialize_deserialize(self):
		try:
			UserEntity(
				FileHandler(),
				json={
				'test user':
				{
				'ahn1':
				{
				'api_key': 'test',
				'date_reset': '2020-05-31',
				'quota': 100,
				'type_map_provider': 'google_maps',
				'usage': {
				'geocoding': 0, 'static_map': 0, 'total': 0
				}
				},
				'ahn2':
				{
				'api_key': 'test',
				'date_reset': '2020-05-31',
				'quota': 100,
				'type_map_provider': 'ahn',
				'usage': {
				'geocoding': 0, 'static_map': 0, 'total': 0
				}
				}
				}
				}
			)
		except Exception:  # pylint: disable=broad-except
			self.fail("myFunc() raised ExceptionType unexpectedly!")
