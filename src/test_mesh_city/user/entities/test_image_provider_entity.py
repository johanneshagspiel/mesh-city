# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest
from datetime import datetime

from parameterized import parameterized

from mesh_city.user.entities.image_provider_entity import ImageProviderEntity
from mesh_city.util.file_handler import FileHandler


class ImageProviderEntityTest(unittest.TestCase):

	@parameterized.expand(
		[
		[datetime(2020, 5, 17), datetime(2020, 5, 31)], [datetime(2020, 2, 1), datetime(2020, 2, 29)],
		[datetime(2019, 2, 1), datetime(2019, 2, 28)],
		]
	)
	def test_end_of_month(self, date, end_date):
		self.assertEqual(ImageProviderEntity.calculate_end_of_month(date), end_date)

	@parameterized.expand(
		[
		[datetime(2020, 5, 17), datetime(2020, 5, 31)], [datetime(2020, 2, 1), datetime(2020, 2, 29)],
		[datetime(2019, 2, 1), datetime(2019, 2, 28)],
		]
	)
	def test_usage_not_reset(self, current_date, date_reset):
		test_usage_dict = {"static_map": 42, "geocoding": 42, "total": 84}
		entity = ImageProviderEntity(
			FileHandler(), type_map_provider="Google Maps", api_key="AIzaSyD9cfAeQKFniipqRUgkcYy1sAtGXJYxNF4", quota=100, date_reset=date_reset
		)
		# circumvents the use of current time in __init__
		entity.date_reset = date_reset
		entity.usage = test_usage_dict
		entity.check_date_reset(current_date)
		self.assertEqual({"static_map": 42, "geocoding": 42, "total": 84}, entity.usage)

	@parameterized.expand(
		[
		[datetime(2020, 6, 17), datetime(2020, 5, 31)], [datetime(2020, 6, 1), datetime(2020, 2, 29)],
		[datetime(2019, 6, 1), datetime(2019, 2, 28)],
		]
	)
	def test_usage_reset(self, current_date, date_reset):
		test_usage_dict = {"static_map": 42, "geocoding": 42, "total": 84}
		entity = ImageProviderEntity(
			FileHandler(), type_map_provider="Google Maps", api_key="AIzaSyD9cfAeQKFniipqRUgkcYy1sAtGXJYxNF4", quota=100, date_reset=date_reset
		)
		# circumvents the use of current time in __init__
		entity.date_reset = date_reset
		entity.usage = test_usage_dict
		entity.check_date_reset(current_date)
		self.assertEqual({"static_map": 0, "geocoding": 0, "total": 0}, entity.usage)

	def test_serialization(self):
		entity = ImageProviderEntity(
			FileHandler(), type_map_provider="Google Maps", api_key="AIzaSyD9cfAeQKFniipqRUgkcYy1sAtGXJYxNF4", quota=100,
		)
		self.assertEqual(
			{
			'api_key': 'AIzaSyD9cfAeQKFniipqRUgkcYy1sAtGXJYxNF4',
			'date_reset': '2020-06-30',
			'quota': 100,
			'type_map_provider': 'Google Maps',
			'usage': {
			'geocoding': 0, 'static_map': 0, 'total': 0
			}
			},
			entity.for_storage()
		)


if __name__ == '__main__':
	unittest.main()
