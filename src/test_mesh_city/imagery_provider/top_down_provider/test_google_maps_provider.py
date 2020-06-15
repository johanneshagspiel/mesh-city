# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest
from pathlib import Path
from unittest import mock

from mesh_city.imagery_provider.top_down_provider.google_maps_provider import GoogleMapsProvider
from mesh_city.user.entities.image_provider_entity import ImageProviderEntity
from mesh_city.util.file_handler import FileHandler


class GoogleMapsProviderTest(unittest.TestCase):

	def setUp(self):
		self.provider = ImageProviderEntity(
			FileHandler(),
			type_map_provider="Google Maps",
			api_key="AIzaSyD9cfAeQKFniipqRUgkcYy1sAtGXJYxNF4",
			quota=500
		)

		self.google_maps_prov = GoogleMapsProvider(self.provider)
		self.longitude = 5
		self.latitude = 50
		self.zoom = 20
		self.file_path = Path.joinpath(Path(__file__).parents[2], "resource_images")

	def mock_response(self):
		mock_resp = mock.Mock()
		path = Path.joinpath(
			Path(__file__).parents[2], "resource_images", "test_mapbox_response_mock.png"
		)
		with open(path, "rb") as img:
			mock_resp.content = img.read()

		return mock_resp

	def test_get_and_store(self):
		g_map = self.google_maps_prov

		g_map.get_and_store_location(
			latitude=self.latitude,
			longitude=self.longitude,
			zoom=self.zoom,
			filename="test_google_top_down.png",
			new_folder_path=self.file_path,
			width=640,
			height=640,
			response=self.mock_response()
		)
		mock_path = Path.joinpath(
			Path(__file__).parents[2], "resource_images", "test_google_top_down_response_mock.png"
		)
		image_path = self.file_path = Path.joinpath(
			Path(__file__).parents[2], "resource_images", "test_google_top_down.png"
		)
		with open(image_path, "rb") as image_one, open(mock_path, "rb") as image_two:
			received_image = image_one.read()
			mock_image = image_two.read()

		self.assertEqual(received_image, mock_image)
