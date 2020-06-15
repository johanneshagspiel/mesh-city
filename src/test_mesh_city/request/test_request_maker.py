# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest
from pathlib import Path
from unittest.mock import Mock

from mesh_city.imagery_provider.top_down_provider.google_maps_provider import GoogleMapsProvider
from mesh_city.request.layers.google_layer import GoogleLayer
from mesh_city.request.request_maker import RequestMaker
from mesh_city.request.request_manager import RequestManager
from mesh_city.user.entities.image_provider_entity import ImageProviderEntity
from mesh_city.util.file_handler import FileHandler


class TestRequestMaker(unittest.TestCase):
	resource_path = Path(__file__).parents[1].joinpath("resources")

	def setUp(self):
		self.request_manager = RequestManager(image_root=self.resource_path)

		self.request_maker = RequestMaker(request_manager=self.request_manager)
		self.request_maker.top_down_provider= GoogleMapsProvider(Mock())
		self.request_maker.image_provider = Mock()

		self.location_input = (-22.824637, -43.242729)
		self.two_coordinate_input = (-22.824637, -43.242729, -22.821384, -43.238813)
		self.coordinate_list = [
			(199167, 296295), (199168, 296295), (199169, 296295), (199170, 296295), (199171, 296295),
			(199172, 296295), (199167, 296296), (199168, 296296), (199169, 296296), (199170, 296296),
			(199171, 296296), (199172, 296296), (199167, 296297), (199168, 296297), (199169, 296297),
			(199170, 296297), (199171, 296297), (199172, 296297), (199167, 296298), (199168, 296298),
			(199169, 296298), (199170, 296298), (199171, 296298), (199172, 296298), (199167,
			296299), (199168, 296299), (199169, 296299), (199170, 296299), (199171,
			296299), (199172, 296299), (199167, 296300), (199168, 296300), (199169,
			296300), (199170, 296300), (199171, 296300), (199172, 296300),
		]

	def test_make_location_request(self):
		request = self.request_maker.make_location_request(
			self.two_coordinate_input[0], self.two_coordinate_input[1],
		)
		self.assertTrue(request.has_layer_of_type(GoogleLayer))

	def test_count_uncached_tiles(self):
		self.assertEqual(
			len(self.coordinate_list), self.request_maker.count_uncached_tiles(self.coordinate_list)
		)

	def test_make_area_request(self):
		request = self.request_maker.make_area_request(
			self.two_coordinate_input[0],
			self.two_coordinate_input[1],
			self.two_coordinate_input[2],
			self.two_coordinate_input[3]
		)
		self.assertTrue(request.has_layer_of_type(GoogleLayer))

	def test_calculate_coordinates_for_rectangle(self):
		list_of_coordinates, _, _= self.request_maker.calculate_coordinates_for_rectangle(
			self.two_coordinate_input[0],
			self.two_coordinate_input[1],
			self.two_coordinate_input[2],
			self.two_coordinate_input[3]
		)
		for (correct_answer, coordinate) in zip(self.coordinate_list, list_of_coordinates):
			self.assertEqual(correct_answer[0], coordinate[0])
			self.assertEqual(correct_answer[1], coordinate[1])

	def test_calculate_coordinates_for_location(self):
		coordinates, _, _ = self.request_maker.calculate_coordinates_for_location(
			self.location_input[0], self.location_input[1]
		)
		self.assertEqual(9, len(coordinates))

	def test_calculate_coordinates_for_rectangle_latitude_flipped(self):
		number_of_images, _, _ = self.request_maker.calculate_coordinates_for_rectangle(
			self.two_coordinate_input[2],
			self.two_coordinate_input[1],
			self.two_coordinate_input[0],
			self.two_coordinate_input[3]
		)
		self.assertEqual(36, len(number_of_images))

	def test_calculate_coordinates_for_rectangle_longitude_flipped(self):
		number_of_images, _, _ = self.request_maker.calculate_coordinates_for_rectangle(
			self.two_coordinate_input[0],
			self.two_coordinate_input[3],
			self.two_coordinate_input[2],
			self.two_coordinate_input[1]
		)
		self.assertEqual(36, len(number_of_images))
