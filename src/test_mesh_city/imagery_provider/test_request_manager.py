# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest
from pathlib import Path
from shutil import rmtree
from unittest.mock import ANY, call, Mock

from mesh_city.imagery_provider.request_manager import RequestManager
from mesh_city.imagery_provider.top_down_provider.google_maps_provider import GoogleMapsProvider
from mesh_city.util.geo_location_util import GeoLocationUtil


class TestRequestManager(unittest.TestCase):

	resource_path = Path(__file__).parents[1].joinpath("resources")

	def setUp(self):
		self.top_down_provider = Mock()
		self.top_down_provider.max_side_resolution_image = 640

		self.two_coordinate_input = ((-22.824637, -43.242729), (-22.821384, -43.238813), 20)
		self.correct_answer = (
			(25, 5, 5),
			[
			((-22.824266172626547, -43.24232666864772), (0, 0)),
			((-22.824266172626547, -43.24152200594317), (1, 0)),
			((-22.824266172626547, -43.240717343238614), (2, 0)),
			((-22.824266172626547, -43.23991268053406), (3, 0)),
			((-22.824266172626547, -43.23910801782951), (4, 0)),
			((-22.823524515859447, -43.24232666864772), (0, 1)),
			((-22.823524515859447, -43.24152200594317), (1, 1)),
			((-22.823524515859447, -43.240717343238614), (2, 1)),
			((-22.823524515859447, -43.23991268053406), (3, 1)),
			((-22.823524515859447, -43.23910801782951), (4, 1)),
			((-22.822782855052044, -43.24232666864772), (0, 2)),
			((-22.822782855052044, -43.24152200594317), (1, 2)),
			((-22.822782855052044, -43.240717343238614), (2, 2)),
			((-22.822782855052044, -43.23991268053406), (3, 2)),
			((-22.822782855052044, -43.23910801782951), (4, 2)),
			((-22.822041190204438, -43.24232666864772), (0, 3)),
			((-22.822041190204438, -43.24152200594317), (1, 3)),
			((-22.822041190204438, -43.240717343238614), (2, 3)),
			((-22.822041190204438, -43.23991268053406), (3, 3)),
			((-22.822041190204438, -43.23910801782951), (4, 3)),
			((-22.821299521316735, -43.24232666864772), (0, 4)),
			((-22.821299521316735, -43.24152200594317), (1, 4)),
			((-22.821299521316735, -43.240717343238614), (2, 4)),
			((-22.821299521316735, -43.23991268053406), (3, 4)),
			((-22.821299521316735, -43.23910801782951), (4, 4)),
			],
		)  # yapf: disable

	def tearDown(self):
		for item in Path(__file__).parents[1].joinpath("resources").glob("*"):
			if item.is_dir():
				rmtree(item)
			else:
				item.unlink()

	def _create_request_manager(
		self, top_down_provider=Mock(), log_manager=Mock(), geo_location_util=Mock()
	):
		return RequestManager(
			user_info=Mock(),
			quota_manager=Mock(),
			top_down_provider=top_down_provider,
			log_manager=log_manager,
			image_util=Mock(),
			geo_location_util=geo_location_util,
			resource_path=self.resource_path,
		)

	def test_calculate_centre_coordinates_two_coordinate_input_correct(self):
		map_entity = Mock(spec=GoogleMapsProvider, wraps=Mock())
		map_entity.max_side_resolution_image = 640
		request_manager = self._create_request_manager(
			top_down_provider=map_entity, geo_location_util=GeoLocationUtil(),
		)

		list_of_coordinates = request_manager.calculate_centre_coordinates_two_coordinate_input(
			self.two_coordinate_input[0], self.two_coordinate_input[1], self.two_coordinate_input[2]
		)

		self.assertEqual(self.correct_answer, list_of_coordinates)

	def test_calculate_centre_coordinates_two_coordinate_input_turned_around(self):
		map_entity = Mock(spec=GoogleMapsProvider, wraps=Mock())
		map_entity.max_side_resolution_image = 640
		request_manager = self._create_request_manager(
			top_down_provider=map_entity, geo_location_util=GeoLocationUtil(),
		)

		list_of_coordinates = request_manager.calculate_centre_coordinates_two_coordinate_input(
			self.two_coordinate_input[1], self.two_coordinate_input[0], self.two_coordinate_input[2]
		)

		self.assertEqual(self.correct_answer, list_of_coordinates)

	def test_calculate_number_of_requested_images_two_coordinate_input(self):
		number_of_images = self._create_request_manager(
			top_down_provider=self.top_down_provider, geo_location_util=GeoLocationUtil(),
		).calculate_number_of_requested_images_two_coordinate_input(
			self.two_coordinate_input[0], self.two_coordinate_input[1], self.two_coordinate_input[2]
		)
		self.assertEqual(25, number_of_images)

	def test_calculate_number_of_requested_images_two_coordinate_input_turned_around(self):
		number_of_images = self._create_request_manager(
			top_down_provider=self.top_down_provider, geo_location_util=GeoLocationUtil(),
		).calculate_number_of_requested_images_two_coordinate_input(
			self.two_coordinate_input[1], self.two_coordinate_input[0], self.two_coordinate_input[2]
		)
		self.assertEqual(25, number_of_images)

	def test_calculate_number_of_requested_images_two_coordinate_input_same_latitude(self):
		number_of_images = self._create_request_manager(
			top_down_provider=self.top_down_provider, geo_location_util=GeoLocationUtil(),
		).calculate_number_of_requested_images_two_coordinate_input(
			self.two_coordinate_input[0],
			(self.two_coordinate_input[0][0], self.two_coordinate_input[1][1]),
			self.two_coordinate_input[2],
		)
		self.assertEqual(5, number_of_images)

	def test_calculate_number_of_requested_images_two_coordinate_input_same_longitude(self):
		number_of_images = self._create_request_manager(
			top_down_provider=self.top_down_provider, geo_location_util=GeoLocationUtil(),
		).calculate_number_of_requested_images_two_coordinate_input(
			self.two_coordinate_input[0],
			(self.two_coordinate_input[1][0], self.two_coordinate_input[0][1]),
			self.two_coordinate_input[2]
		)
		self.assertEqual(5, number_of_images)
