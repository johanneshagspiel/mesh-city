# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest

from mesh_city.imagery_provider.top_down_provider.ahn_provider import AhnProvider
from mesh_city.imagery_provider.top_down_provider_factory import TopDownProviderFactory
from mesh_city.user.entities.image_provider_entity import ImageProviderEntity
from mesh_city.util.file_handler import FileHandler


class ProviderFactoryTest(unittest.TestCase):

	def test_construct_image_provider_right(self):
		top_down_factory = TopDownProviderFactory()
		entity = ImageProviderEntity(
			FileHandler(), type_map_provider="ahn", api_key="test", quota="200"
		)
		self.assertIsInstance(top_down_factory.get_top_down_provider(entity), AhnProvider)

	def test_construct_image_provider_wrong(self):

		self.assertRaises(ValueError, ImageProviderEntity,
			FileHandler(),
			type_map_provider="this_is_an_undefined_image_provider_type",
			api_key="test",
			quota="200"
		)
