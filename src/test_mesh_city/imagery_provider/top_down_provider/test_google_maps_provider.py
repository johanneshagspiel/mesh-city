import unittest
from datetime import datetime
from pathlib import Path
from unittest import mock

from mesh_city.imagery_provider.top_down_provider.google_maps_provider import GoogleMapsProvider
from mesh_city.user.entities.image_provider_entity import ImageProviderEntity
from mesh_city.util.file_handler import FileHandler


class GoogleMapsProviderTest(unittest.TestCase):

	def setUp(self):
		self.provider = ImageProviderEntity(
			FileHandler(),
			type_map_provider="google_maps",
			api_key="AIzaSyD9cfAeQKFniipqRUgkcYy1sAtGXJYxNF4",
			quota=500,
			usage=None,
			date_reset=datetime(2019, 2, 28)
		)

		self.google_maps_prov = GoogleMapsProvider(self.provider)
		self.longitude = (11.999212921106265, 11.999195337295573)
		self.latitude = (12.000787078893735, 12.000804662704427)
		self.zoom = 2
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
