# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest
from datetime import datetime
from pathlib import Path
from shutil import rmtree
from unittest.mock import Mock

from mesh_city.application import Application
from mesh_city.imagery_provider.top_down_provider.google_maps_provider import GoogleMapsProvider
from mesh_city.user.entities.image_provider_entity import ImageProviderEntity
from mesh_city.user.entities.user_entity import UserEntity
from mesh_city.util.file_handler import FileHandler


class TestRequestManager(unittest.TestCase):

	resource_path = Path(__file__).parents[1].joinpath("resources")

	def setUp(self):

		self.provider1 = ImageProviderEntity(
			FileHandler(),
			type_map_provider="google_maps",
			api_key="AIzaSyD9cfAeQKFniipqRUgkcYy1sAtGXJYxNF4",
			quota=100,
			date_reset=datetime(2019, 2, 28)
		)
		provider_dict = {"google_maps": self.provider1}
		self.user_entity = UserEntity(
			FileHandler(), name="test user", image_providers=provider_dict
		)

		self.application = Application()
		self.application.late_init(self.user_entity)

		self.request_manager = self.application.request_manager
		self.request_manager.top_down_provider = GoogleMapsProvider(
			image_provider_entity=self.provider1
		)

		self.location_input = (-22.824637, -43.242729)

		self.two_coordinate_input = (-22.824637, -43.242729, -22.821384, -43.238813)
		self.correct_answer = (
			[(2.0, 2.0),
			(-22.824605342539485, -43.242530822753906),
			(-22.824605342539485, -43.241837310791),
			(-22.824605342539485, -43.241150665283186),
			(-22.823978791021894, -43.242530822753906),
			(-22.823978791021894, -43.241837310791),
			(-22.823978791021894, -43.241150665283186),
			(-22.823345907773717, -43.242530822753906),
			(-22.823345907773717, -43.241837310791),
			(-22.823345907773717, -43.241150665283186),
			(-22.824605342539485, -43.240464019775374),
			(-22.824605342539485, -43.23977737426756),
			(-22.824605342539485, -43.23909072875975),
			(-22.823978791021894, -43.240464019775374),
			(-22.823978791021894, -43.23977737426756),
			(-22.823978791021894, -43.23909072875975),
			(-22.823345907773717, -43.240464019775374),
			(-22.823345907773717, -43.23977737426756),
			(-22.823345907773717, -43.23909072875975),
			(-22.82271302158353, -43.242530822753906),
			(-22.82271302158353, -43.241837310791),
			(-22.82271302158353, -43.241150665283186),
			(-22.822080132451397, -43.242530822753906),
			(-22.822080132451397, -43.241837310791),
			(-22.822080132451397, -43.241150665283186),
			(-22.82144724037738, -43.242530822753906),
			(-22.82144724037738, -43.241837310791),
			(-22.82144724037738, -43.241150665283186),
			(-22.82271302158353, -43.240464019775374),
			(-22.82271302158353, -43.23977737426756),
			(-22.82271302158353, -43.23909072875975),
			(-22.822080132451397, -43.240464019775374),
			(-22.822080132451397, -43.23977737426756),
			(-22.822080132451397, -43.23909072875975),
			(-22.82144724037738, -43.240464019775374),
			(-22.82144724037738, -43.23977737426756),
			(-22.82144724037738, -43.23909072875975)]
		)  # yapf: disable

	def tearDown(self):
		for item in Path(__file__).parents[1].joinpath("resources").glob("*"):
			if item.is_dir():
				rmtree(item)
			else:
				item.unlink()

	def test_calculate_centre_coordinates_two_coordinate_input_correct(self):
		map_entity = Mock(spec=GoogleMapsProvider, wraps=Mock())
		map_entity.max_side_resolution_image = 640
		request_manager = self.application.request_manager

		list_of_coordinates = request_manager.calculate_locations(
			[
			self.two_coordinate_input[0],
			self.two_coordinate_input[1],
			self.two_coordinate_input[2],
			self.two_coordinate_input[3]
			]
		)

		for (correct_answer, coordinate) in zip(self.correct_answer, list_of_coordinates):
			self.assertAlmostEqual(correct_answer[0], coordinate[0], places=6)
			self.assertAlmostEqual(correct_answer[1], coordinate[1], places=6)

	def test_calculate_number_of_requested_images_two_coordinate_input(self):
		number_of_images = self.application.request_manager.calculate_locations(
			self.two_coordinate_input
		)
		self.assertEqual(37, len(number_of_images))

	def test_calculate_centre_coordinates_two_coordinate_input_latitude_turned_around(self):
		number_of_images = self.application.request_manager.calculate_locations(
			[
			self.two_coordinate_input[2],
			self.two_coordinate_input[1],
			self.two_coordinate_input[0],
			self.two_coordinate_input[3]
			]
		)
		self.assertEqual(37, len(number_of_images))

	def test_calculate_number_of_requested_images_two_coordinate_longitude_turned_around(self):
		number_of_images = self.application.request_manager.calculate_locations(
			[
			self.two_coordinate_input[0],
			self.two_coordinate_input[3],
			self.two_coordinate_input[2],
			self.two_coordinate_input[1]
			]
		)
		self.assertEqual(37, len(number_of_images))

	def test_calculate_number_of_requested_images_two_coordinate_input_same_latitude(self):
		with self.assertRaises(Exception):
			self.application.request_manager.calculate_locations(
				[
				self.two_coordinate_input[0],
				self.two_coordinate_input[1],
				self.two_coordinate_input[0],
				self.two_coordinate_input[3]
				]
			)

	def test_calculate_number_of_requested_images_two_coordinate_input_same_longitude(self):
		with self.assertRaises(Exception):
			self.application.request_manager.calculate_locations(
				[
				self.two_coordinate_input[0],
				self.two_coordinate_input[1],
				self.two_coordinate_input[2],
				self.two_coordinate_input[1]
				]
			)

	def test_single_request(self):
		request_manager = self.request_manager
		request_manager.top_down_provider = Mock()

		request_manager.top_down_provider.get_and_store_location(
			(52.010442, 4.357480), 1.0, 400, 600
		)

		self.request_manager.top_down_provider.get_and_store_location.assert_called_once_with(
			(52.010442, 4.357480), 1.0, 400, 600
		)
