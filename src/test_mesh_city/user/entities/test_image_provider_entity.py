# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest
from datetime import datetime

from parameterized import parameterized

from mesh_city.imagery_provider.top_down_provider.ahn_provider import AhnProvider
from mesh_city.user.entities.image_provider_entity import ImageProviderEntity
from mesh_city.util.file_handler import FileHandler


class ImageProviderEntityTest(unittest.TestCase):
	@parameterized.expand(
		[
			[datetime(2020, 5, 17),datetime(2020, 5, 31)],
			[datetime(2020, 2, 1),datetime(2020, 2, 29)],
			[datetime(2019, 2, 1), datetime(2019, 2, 28)],
		]
	)
	def test_end_of_month(self,date,end_date):
		self.assertEqual(
			ImageProviderEntity.calculate_end_of_month(date),
			end_date
		)
	@parameterized.expand(
		[
			[datetime(2020, 5, 17),datetime(2020, 5, 31)],
			[datetime(2020, 2, 1),datetime(2020, 2, 29)],
			[datetime(2019, 2, 1), datetime(2019, 2, 28)],
		]
	)
	def test_usage_not_reset(self,current_date,date_reset):
		test_usage_dict = {"static_map": 42, "geocoding": 42, "total": 84}
		entity = ImageProviderEntity(FileHandler(),type="test",api_key="test",quota=100,usage=None,date_reset=date_reset)
		# circumvents the use of current time in __init__
		entity.date_reset = date_reset
		entity.usage = test_usage_dict
		entity.check_date_reset(current_date)
		self.assertEqual(
			{"static_map": 42, "geocoding": 42, "total": 84},
			entity.usage
		)

	@parameterized.expand(
		[
			[datetime(2020, 6, 17),datetime(2020, 5, 31)],
			[datetime(2020,6, 1),datetime(2020, 2, 29)],
			[datetime(2019, 6, 1), datetime(2019, 2, 28)],
		]
	)
	def test_usage_reset(self,current_date,date_reset):
		test_usage_dict = {"static_map": 42, "geocoding": 42, "total": 84}
		entity = ImageProviderEntity(FileHandler(),type="test",api_key="test",quota=100,usage=None,date_reset=date_reset)
		# circumvents the use of current time in __init__
		entity.date_reset = date_reset
		entity.usage = test_usage_dict
		entity.check_date_reset(current_date)
		self.assertEqual(
			{"static_map": 0, "geocoding": 0, "total": 0},
			entity.usage
		)

	@parameterized.expand(
		[
			[datetime(2020, 6, 17),AhnProvider],
			[datetime(2020,6, 1),datetime(2020, 2, 29)],
			[datetime(2019, 6, 1), datetime(2019, 2, 28)],
		]
	)
	def test_construct_image_provider_right(self,type,corresponding_type):
		self.assertIsInstance(self.number, int)
		entity = ImageProviderEntity(FileHandler(),type=type,api_key="test",quota=100,usage=None,date_reset=None)
		self.assertRaises(
			ValueError,
			entity.construct_image_provider
		)

	def test_construct_image_provider_wrong(self):
		entity = ImageProviderEntity(FileHandler(),type="this_is_an_undefined_image_provider_type",api_key="test",quota=100,usage=None,date_reset=None)
		self.assertRaises(
			ValueError,
			entity.construct_image_provider
		)

if __name__ == '__main__':
    unittest.main()
