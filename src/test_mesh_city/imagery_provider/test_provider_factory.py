# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest
from datetime import datetime

from parameterized import parameterized

from mesh_city.imagery_provider.top_down_provider.ahn_provider import AhnProvider
from mesh_city.imagery_provider.top_down_provider_factory import TopDownProviderFactory
from mesh_city.user.entities.image_provider_entity import ImageProviderEntity
from mesh_city.util.file_handler import FileHandler


class ProviderFactoryTest(unittest.TestCase):

	def test_construct_image_provider_right(self):
		top_down_factory = TopDownProviderFactory()
		entity = ImageProviderEntity(
			FileHandler(), type="ahn", api_key="test", quota=100, usage=None, date_reset=None
		)
		self.assertIsInstance(top_down_factory.get_top_down_provider(entity), AhnProvider)

	def test_construct_image_provider_wrong(self):
		top_down_factory = TopDownProviderFactory()
		entity = ImageProviderEntity(
			FileHandler(),
			type="this_is_an_undefined_image_provider_type",
			api_key="test",
			quota=100,
			usage=None,
			date_reset=None
		)
		self.assertRaises(ValueError, top_down_factory.get_top_down_provider, entity)
