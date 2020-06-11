# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest
from pathlib import Path
from shutil import rmtree
from unittest.mock import Mock

from mesh_city.imagery_provider.top_down_provider.google_maps_provider import GoogleMapsProvider
from mesh_city.request.request_maker import RequestMaker
from mesh_city.request.request_manager import RequestManager
from mesh_city.util.file_handler import FileHandler


class TestRequestMaker(unittest.TestCase):

	resource_path = Path(__file__).parents[1].joinpath("resources")

	def setUp(self):
		self.request_manager = RequestManager
		imagery_provider = Mock(spec=GoogleMapsProvider)
		imagery_provider.max_zoom = 20
		self.request_maker = RequestMaker(FileHandler())
		self.request_maker.set_top_down_provider(imagery_provider)
		self.location_input = (-22.824637, -43.242729)
		self.two_coordinate_input = (-22.824637, -43.242729, -22.821384, -43.238813)
		self.correct_answer = [
				(199167, 296295),
				(199168, 296295),
				(199169, 296295),
				(199170, 296295),
				(199171, 296295),
				(199172, 296295),
				(199167, 296296),
				(199168, 296296),
				(199169, 296296),
				(199170, 296296),
				(199171, 296296),
				(199172, 296296),
				(199167, 296297),
				(199168, 296297),
				(199169, 296297),
				(199170, 296297),
				(199171, 296297),
				(199172, 296297),
				(199167, 296298),
				(199168, 296298),
				(199169, 296298),
				(199170, 296298),
				(199171, 296298),
				(199172, 296298),
				(199167, 296299),
				(199168, 296299),
				(199169, 296299),
				(199170, 296299),
				(199171, 296299),
				(199172, 296299),
				(199167, 296300),
				(199168, 296300),
				(199169, 296300),
				(199170, 296300),
				(199171, 296300),
				(199172, 296300),]

	def tearDown(self):
		for item in Path(__file__).parents[1].joinpath("resources").glob("*"):
			if item.is_dir():
				rmtree(item)
			else:
				item.unlink()

	def test_calculate_centre_coordinates_two_coordinate_input_correct(self):
		map_entity = Mock(spec=GoogleMapsProvider, wraps=Mock())
		map_entity.max_side_resolution_image = 640
		request_manager = self.request_maker
		list_of_coordinates, width, height = request_manager.calculate_coordinates_for_rectangle(
			self.two_coordinate_input[0],
			self.two_coordinate_input[1],
			self.two_coordinate_input[2],
			self.two_coordinate_input[3]
		)
		for (correct_answer, coordinate) in zip(self.correct_answer, list_of_coordinates):
			self.assertEqual(correct_answer[0], coordinate[0])
			self.assertEqual(correct_answer[1], coordinate[1])

	def test_calculate_number_of_requested_images_two_coordinate_input(self):
		coordinates, width, height = self.request_maker.calculate_coordinates_for_location(
			self.location_input[0],self.location_input[1]
		)
		self.assertEqual(9, len(coordinates))
