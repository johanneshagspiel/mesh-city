# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest
from pathlib import Path
from shutil import rmtree
from unittest.mock import ANY, call, Mock

from mesh_city.imagery_provider.request_manager import RequestManager
from mesh_city.imagery_provider.top_down_provider.google_maps_provider import GoogleMapsProvider
from mesh_city.util.file_handler import FileHandler
from mesh_city.util.geo_location_util import GeoLocationUtil


class TestRequestManager(unittest.TestCase):
	resource_path = Path(__file__).parents[1].joinpath("resources")

	def setUp(self):
		self.top_down_provider = Mock()
		self.top_down_provider.max_side_resolution_image = 640

		self.two_coordinate_input = ((51.913205, 4.453749), (51.912532, 4.456339), 20)
		self.correct_answer = ((8, 2, 4),
			[((51.9131439404174, 4.453926086425781), (268630, 173385)),
			((51.9131439404174, 4.454619598388689), (268631, 173385)),
			((51.9131439404174, 4.455306243896501), (268632, 173385)),
			((51.9131439404174, 4.455992889404314), (268633, 173385)),
			((51.91271614182748, 4.453926086425781), (268630, 173386)),
			((51.91271614182748, 4.454619598388689), (268631, 173386)),
			((51.91271614182748, 4.455306243896501), (268632, 173386)),
			((51.91271614182748, 4.455992889404314), (268633, 173386))])  # yapf: disable
		self.two_coordinate_input_quad = (
			(50.000236394207846, 4.9994659423828125), (49.99979061343613, 5.00015955434572), 20
		)
		self.correct_answer_quad = (
			(4, 2, 2),
			[
			((50.00067775723634, 4.9994659423828125), (269425, 177808)),
			((50.00067775723634, 5.00015945434572), (269426, 177808)),
			((50.00023198055709, 4.9994659423828125), (269425, 177809)),
			((50.00023198055709, 5.00015945434572), (269426, 177809))
			]
		)
		self.correct_answer_quad_block = [
			(1.0, 1.0),
			(49.99957434206772, 4.999809265136719),
			(49.99957434206772, 5.000502777099626),
			(49.99957434206772, 5.001189422607439),
			(50.00001129750311, 4.999809265136719),
			(50.00001129750311, 5.000502777099626),
			(50.00001129750311, 5.001189422607439),
			(50.000452662598086, 4.999809265136719),
			(50.000452662598086, 5.000502777099626),
			(50.000452662598086, 5.001189422607439)]  # yapf: disable

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
			file_handler=FileHandler(root=Path(__file__).parents[1]),
			top_down_provider=top_down_provider,
			log_manager=log_manager,
			image_util=Mock(),
			geo_location_util=geo_location_util,
		)

	def test_calculate_centre_coordinates_two_coordinate_input_correct(self):
		map_entity = Mock(spec=GoogleMapsProvider, wraps=Mock())
		request_manager = self._create_request_manager(
			top_down_provider=map_entity, geo_location_util=GeoLocationUtil(),
		)

		list_of_coordinates = request_manager.calculate_centre_coordinates_two_coordinate_input(
			self.two_coordinate_input[0], self.two_coordinate_input[1], self.two_coordinate_input[2]
		)

		self.assertEqual(self.correct_answer, list_of_coordinates)

	def test_calculate_centre_coordinates_two_coordinate_input_turned_around(self):
		map_entity = Mock(spec=GoogleMapsProvider, wraps=Mock())
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
		self.assertEqual(self.correct_answer[0][0], number_of_images)

	def test_calculate_number_of_requested_images_two_coordinate_input_turned_around(self):
		number_of_images = self._create_request_manager(
			top_down_provider=self.top_down_provider, geo_location_util=GeoLocationUtil(),
		).calculate_number_of_requested_images_two_coordinate_input(
			self.two_coordinate_input[1], self.two_coordinate_input[0], self.two_coordinate_input[2]
		)
		self.assertEqual(self.correct_answer[0][0], number_of_images)

	def test_calculate_number_of_requested_images_two_coordinate_input_same_latitude(self):
		number_of_images = self._create_request_manager(
			top_down_provider=self.top_down_provider, geo_location_util=GeoLocationUtil(),
		).calculate_number_of_requested_images_two_coordinate_input(
			self.two_coordinate_input[0],
			(self.two_coordinate_input[0][0], self.two_coordinate_input[1][1]),
			self.two_coordinate_input[2],
		)
		self.assertEqual(self.correct_answer[0][2], number_of_images)

	def test_calculate_number_of_requested_images_two_coordinate_input_same_longitude(self):
		number_of_images = self._create_request_manager(
			top_down_provider=self.top_down_provider, geo_location_util=GeoLocationUtil(),
		).calculate_number_of_requested_images_two_coordinate_input(
			self.two_coordinate_input[0],
			(self.two_coordinate_input[1][0], self.two_coordinate_input[0][1]),
			self.two_coordinate_input[2]
		)
		self.assertEqual(self.correct_answer[0][1], number_of_images)

	def test_calculate_centre_coordinates_two_coordinate_input_block(self):
		coordinates = self._create_request_manager(
			top_down_provider=self.top_down_provider, geo_location_util=GeoLocationUtil(),
		).calculate_centre_coordinates_two_coordinate_input_block(
			self.two_coordinate_input_quad[0],
			self.two_coordinate_input_quad[1],
			self.two_coordinate_input_quad[2]
		)
		self.assertEqual(self.correct_answer_quad_block, coordinates)

	def test_single_request(self):
		request_manager = self._create_request_manager(top_down_provider=self.top_down_provider)

		request_manager.make_single_request((52.010442, 4.357480), 1.0, 400, 600)

		self.top_down_provider.get_and_store_location.assert_called_once_with(
			latitude=52.010442,
			longitude=4.357480,
			zoom=1.0,
			filename="52.010442, 4.35748.png",
			height=400,
			width=600,
			new_folder_path=ANY,
		)

	# def test_bounding_box_request_bottom_left_top_right(self):
	# 	self.top_down_provider.max_zoom = 20.0
	# 	request_manager = self._create_request_manager(
	# 		top_down_provider=self.top_down_provider, geo_location_util=GeoLocationUtil()
	# 	)
	#
	# 	request_manager.make_request_two_coordinates(
	# 		(self.two_coordinate_input_quad[0][0], self.two_coordinate_input_quad[0][1]),
	# 		(self.two_coordinate_input_quad[1][0], self.two_coordinate_input_quad[1][1]),
	# 		self.two_coordinate_input_quad[2]
	# 	)
		# print("4_" + str(self.correct_answer_quad[1][3][1][0]) + ","
		# 			         + str(self.correct_answer_quad[1][3][1][1]) + "_"
		# 			         + str(self.correct_answer_quad[1][3][0][0]) + ","
		# 			         + str(self.correct_answer_quad[1][3][0][1]) + ".png",)
		# print([call(
		# 			latitude=self.correct_answer_quad[1][0][0][0],
		# 			longitude=self.correct_answer_quad[1][0][0][1],
		# 			zoom=20,
		# 			filename="1_" + str(self.correct_answer_quad[1][0][1][0]) + ","
		# 			         + str(self.correct_answer_quad[1][0][1][1]) + "_"
		# 			         + str(self.correct_answer_quad[1][0][0][0]) + ","
		# 			         + str(self.correct_answer_quad[1][0][0][1]) + ".png",
		# 			new_folder_path=ANY,
		# 		),
		# 		call(
		# 			latitude=self.correct_answer_quad[1][1][0][0],
		# 			longitude=self.correct_answer_quad[1][1][0][1],
		# 			zoom=20.0,
		# 			filename="2_" + str(self.correct_answer_quad[1][1][1][0]) + ","
		# 			         + str(self.correct_answer_quad[1][1][1][1]) + "_"
		# 			         + str(self.correct_answer_quad[1][1][0][0]) + ","
		# 			         + str(self.correct_answer_quad[1][1][0][1]) + ".png",
		# 			new_folder_path=ANY,
		# 		),
		# 		call(
		# 			latitude=self.correct_answer_quad[1][2][0][0],
		# 			longitude=self.correct_answer_quad[1][2][0][1],
		# 			zoom=20.0,
		# 			filename="3_" + str(self.correct_answer_quad[1][2][1][0]) + ","
		# 			         + str(self.correct_answer_quad[1][2][1][1]) + "_"
		# 			         + str(self.correct_answer_quad[1][2][0][0]) + ","
		# 			         + str(self.correct_answer_quad[1][2][0][1]) + ".png",
		# 			new_folder_path=ANY,
		# 		),
		# 		call(
		# 			latitude=self.correct_answer_quad[1][3][0][0],
		# 			longitude=self.correct_answer_quad[1][3][0][1],
		# 			zoom=20.0,
		# 			filename="4_" + str(self.correct_answer_quad[1][3][1][0]) + ","
		# 			         + str(self.correct_answer_quad[1][3][1][1]) + "_"
		# 			         + str(self.correct_answer_quad[1][3][0][0]) + ","
		# 			         + str(self.correct_answer_quad[1][3][0][1]) + ".png",
		# 			new_folder_path=ANY,
		# 		),
		# 	])
		#
		# self.top_down_provider.get_and_store_location.assert_has_calls(
		# 	calls=[
		# 	call(
		# 	latitude=self.correct_answer_quad[1][0][0][0],
		# 	longitude=self.correct_answer_quad[1][0][0][1],
		# 	zoom=20,
		# 	filename="1_" + str(self.correct_answer_quad[1][0][1][0]) + "," +
		# 	str(self.correct_answer_quad[1][0][1][1]) + "_" +
		# 	str(self.correct_answer_quad[1][0][0][0]) + "," +
		# 	str(self.correct_answer_quad[1][0][0][1]) + ".png",
		# 	new_folder_path=ANY,
		# 	),
		# 	call(
		# 	latitude=self.correct_answer_quad[1][1][0][0],
		# 	longitude=self.correct_answer_quad[1][1][0][1],
		# 	zoom=20.0,
		# 	filename="2_" + str(self.correct_answer_quad[1][1][1][0]) + "," +
		# 	str(self.correct_answer_quad[1][1][1][1]) + "_" +
		# 	str(self.correct_answer_quad[1][1][0][0]) + "," +
		# 	str(self.correct_answer_quad[1][1][0][1]) + ".png",
		# 	new_folder_path=ANY,
		# 	),
		# 	call(
		# 	latitude=self.correct_answer_quad[1][2][0][0],
		# 	longitude=self.correct_answer_quad[1][2][0][1],
		# 	zoom=20.0,
		# 	filename="3_" + str(self.correct_answer_quad[1][2][1][0]) + "," +
		# 	str(self.correct_answer_quad[1][2][1][1]) + "_" +
		# 	str(self.correct_answer_quad[1][2][0][0]) + "," +
		# 	str(self.correct_answer_quad[1][2][0][1]) + ".png",
		# 	new_folder_path=ANY,
		# 	),
		# 	call(
		# 	latitude=self.correct_answer_quad[1][3][0][0],
		# 	longitude=self.correct_answer_quad[1][3][0][1],
		# 	zoom=20.0,
		# 	filename="4_" + str(self.correct_answer_quad[1][3][1][0]) + "," +
		# 	str(self.correct_answer_quad[1][3][1][1]) + "_" +
		# 	str(self.correct_answer_quad[1][3][0][0]) + "," +
		# 	str(self.correct_answer_quad[1][3][0][1]) + ".png",
		# 	new_folder_path=ANY,
		# 	),
		# 	],
		# 	any_order=True,
		# )
