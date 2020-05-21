# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest
from pathlib import Path
from shutil import rmtree

from mesh_city.imagery_provider.request_manager import RequestManager
from mesh_city.imagery_provider.top_down_provider.google_maps_provider import GoogleMapsProvider
from mesh_city.logs.log_manager import LogManager
from mesh_city.user.quota_manager import QuotaManager
from mesh_city.user.user_info import UserInfo
from mesh_city.util.geo_location_util import GeoLocationUtil
from mesh_city.util.image_util import ImageUtil


class TestRequestManager(unittest.TestCase):

	class MockTopDownProvider:

		def __init__(self):
			self.max_zoom = None
			self.max_side_resolution_image = None
			self.padding = None
			self.name = None
			self.given_arguments = {"get_and_store_location": []}

		def get_and_store_location(
			self, latitude, longitude, zoom, filename, new_folder_path, width=None, height=None
		):
			self.given_arguments["get_and_store_location"].append(
				{
				"latitude": latitude,
				"longitude": longitude,
				"zoom": zoom,
				"new_folder_path": new_folder_path,
				"filename": filename,
				"width": width,
				"height": height,
				}
			)

	class MockImageUtil:

		def __init__(self):
			self.given_arguments = {"concat_images": []}

		def concat_images(self, new_folder_path, request, tile_number):
			self.given_arguments["concat_images"].append(
				{
				"new_folder_path": new_folder_path, "request": request, "tile_number": tile_number,
				}
			)

	class MockLogManager:

		def __init__(self):
			self.given_arguments = {"write_entry_log": []}

		def write_entry_log(self, log_entry):
			self.given_arguments["write_entry_log"].append({"log_entry": log_entry})

		def get_request_number(self):
			return 1

	def setUp(self):
		self.resource_path = Path(__file__).parents[1].joinpath("resources")
		self.user_info = UserInfo(
			"Blue", "AIzaSyD9cfAeQKFniipqRUgkcYy1sAtGXJYxNF4", 500, 25, 1452, 8, 15, 10, 55, 42
		)
		self.quota_manager = QuotaManager(self.user_info)
		self.request_manager = RequestManager(
			user_info=self.user_info,
			quota_manager=self.quota_manager,
			map_entity=GoogleMapsProvider(user_info=self.user_info, quota_manager=self.quota_manager),
			log_manager=LogManager(),
			image_util=ImageUtil(),
			geo_location_util=GeoLocationUtil(),
		)
		self.two_coordinate_input = (-22.824637, -43.242729), (-22.821384, -43.238813), 20
		self.correct_answer = (
			(25, 5, 5),
			[
			((-22.824266172626547, -43.24232666864772), (0,0)),
			((-22.824266172626547, -43.24152200594317), (1,0)),
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
			]
		)  # yapf: disable

	def tearDown(self):
		for item in Path(__file__).parents[1].joinpath("resources").glob("*"):
			rmtree(item) if item.is_dir() else item.unlink()

	def test_calculate_centre_coordinates_two_coordinate_input_correct(self):
		list_of_coordinates = self.request_manager.calculate_centre_coordinates_two_coordinate_input(
			self.two_coordinate_input[0], self.two_coordinate_input[1], self.two_coordinate_input[2]
		)
		self.assertEqual(self.correct_answer, list_of_coordinates)

	def test_calculate_centre_coordinates_two_coordinate_input_turned_around(self):
		list_of_coordinates = self.request_manager.calculate_centre_coordinates_two_coordinate_input(
			self.two_coordinate_input[1], self.two_coordinate_input[0], self.two_coordinate_input[2]
		)
		self.assertEqual(self.correct_answer, list_of_coordinates)

	def test_calculate_number_of_requested_images_two_coordinate_input(self):
		number_of_images = self.request_manager.calculate_number_of_requested_images_two_coordinate_input(
			self.two_coordinate_input[0], self.two_coordinate_input[1], self.two_coordinate_input[2]
		)
		self.assertEqual(25, number_of_images)

	def test_calculate_number_of_requested_images_two_coordinate_input_turned_around(self):
		number_of_images = self.request_manager.calculate_number_of_requested_images_two_coordinate_input(
			self.two_coordinate_input[1], self.two_coordinate_input[0], self.two_coordinate_input[2]
		)
		self.assertEqual(25, number_of_images)

	def test_calculate_number_of_requested_images_two_coordinate_input_same_latitude(self):
		number_of_images = self.request_manager.calculate_number_of_requested_images_two_coordinate_input(
			self.two_coordinate_input[0],
			(self.two_coordinate_input[0][0], self.two_coordinate_input[1][1]),
			self.two_coordinate_input[2]
		)
		self.assertEqual(5, number_of_images)

	def test_calculate_number_of_requested_images_two_coordinate_input_same_longitude(self):
		number_of_images = self.request_manager.calculate_number_of_requested_images_two_coordinate_input(
			self.two_coordinate_input[0],
			(self.two_coordinate_input[1][0], self.two_coordinate_input[0][1]),
			self.two_coordinate_input[2]
		)
		self.assertEqual(5, number_of_images)

	def test_single_request(self):
		top_down_provider = TestRequestManager.MockTopDownProvider()
		request_manager = RequestManager(
			user_info=self.user_info,
			quota_manager=self.quota_manager,
			map_entity=top_down_provider,
			log_manager=LogManager(resource_path=self.resource_path),
			image_util=ImageUtil(resource_path=self.resource_path),
			geo_location_util=GeoLocationUtil(),
			resource_path=self.resource_path,
		)

		request_manager.make_single_request((52.010442, 4.357480), 1.0, 400, 600)

		given_arguments = top_down_provider.given_arguments["get_and_store_location"][0]
		self.assertEqual(given_arguments["latitude"], 52.010442)
		self.assertEqual(given_arguments["longitude"], 4.357480)
		self.assertEqual(given_arguments["zoom"], 1.0)
		self.assertEqual(given_arguments["filename"], "52.010442, 4.35748.png")
		self.assertEqual(given_arguments["height"], 400)
		self.assertEqual(given_arguments["width"], 600)

	def test_bounding_box_request_bottom_left_top_right(self):
		top_down_provider = TestRequestManager.MockTopDownProvider()
		top_down_provider.max_zoom = 14.0
		top_down_provider.max_side_resolution_image = 500
		request_manager = RequestManager(
			user_info=self.user_info,
			quota_manager=self.quota_manager,
			map_entity=top_down_provider,
			log_manager=LogManager(resource_path=self.resource_path),
			image_util=ImageUtil(resource_path=self.resource_path),
			geo_location_util=GeoLocationUtil(),
			resource_path=self.resource_path,
		)

		request_manager.make_request_two_coordinates((51.989954, 4.330746), (52.021186, 4.374115))

		given_arguments = top_down_provider.given_arguments["get_and_store_location"]
		self.assertEqual(given_arguments[0]["latitude"], 52.00316762660327)
		self.assertEqual(given_arguments[0]["longitude"], 4.352203672121509)
		self.assertEqual(given_arguments[0]["zoom"], 14.0)
		self.assertEqual(
			given_arguments[0]["filename"], "1_0,0_52.00316762660327,4.352203672121509.png"
		)
		self.assertEqual(given_arguments[1]["latitude"], 52.00316762660327)
		self.assertEqual(given_arguments[1]["longitude"], 4.395119016364525)
		self.assertEqual(given_arguments[1]["zoom"], 14.0)
		self.assertEqual(
			given_arguments[1]["filename"], "2_1,0_52.00316762660327,4.395119016364525.png"
		)
		self.assertEqual(given_arguments[2]["latitude"], 52.02958708108182)
		self.assertEqual(given_arguments[2]["longitude"], 4.352203672121509)
		self.assertEqual(given_arguments[2]["zoom"], 14.0)
		self.assertEqual(
			given_arguments[2]["filename"], "3_0,1_52.02958708108182,4.352203672121509.png"
		)
		self.assertEqual(given_arguments[3]["latitude"], 52.02958708108182)
		self.assertEqual(given_arguments[3]["longitude"], 4.395119016364525)
		self.assertEqual(given_arguments[3]["zoom"], 14.0)
		self.assertEqual(
			given_arguments[3]["filename"], "4_1,1_52.02958708108182,4.395119016364525.png"
		)

	def test_request_block_centre_coordinates(self):
		top_down_provider = TestRequestManager.MockTopDownProvider()
		top_down_provider.padding = 0
		top_down_provider.name = "mock"
		request_manager = RequestManager(
			user_info=self.user_info,
			quota_manager=self.quota_manager,
			map_entity=top_down_provider,
			log_manager=TestRequestManager.MockLogManager(),
			image_util=TestRequestManager.MockImageUtil(),
			geo_location_util=GeoLocationUtil(),
			resource_path=self.resource_path,
		)

		request_manager.make_request_for_block(centre_coordinates=(51.989954, 4.330746), zoom=20.0)

		given_arguments = top_down_provider.given_arguments["get_and_store_location"]
		self.assertEqual(given_arguments[0]["latitude"], 51.98942545493587)
		self.assertEqual(given_arguments[0]["longitude"], 4.32988769311514)
		self.assertEqual(given_arguments[1]["latitude"], 51.98942545493587)
		self.assertEqual(given_arguments[1]["longitude"], 4.330746)
		self.assertEqual(given_arguments[2]["latitude"], 51.98942545493587)
		self.assertEqual(given_arguments[2]["longitude"], 4.331604306884861)
		self.assertEqual(given_arguments[3]["latitude"], 51.989954)
		self.assertEqual(given_arguments[3]["longitude"], 4.32988769311514)
		self.assertEqual(given_arguments[4]["latitude"], 51.989954)
		self.assertEqual(given_arguments[4]["longitude"], 4.330746)
		self.assertEqual(given_arguments[5]["latitude"], 51.989954)
		self.assertEqual(given_arguments[5]["longitude"], 4.331604306884861)
		self.assertEqual(given_arguments[6]["latitude"], 51.990482545064125)
		self.assertEqual(given_arguments[6]["longitude"], 4.32988769311514)
		self.assertEqual(given_arguments[7]["latitude"], 51.990482545064125)
		self.assertEqual(given_arguments[7]["longitude"], 4.330746)
		self.assertEqual(given_arguments[8]["latitude"], 51.990482545064125)
		self.assertEqual(given_arguments[8]["longitude"], 4.331604306884861)

	def test_request_block_bounding_box(self):
		top_down_provider = TestRequestManager.MockTopDownProvider()
		top_down_provider.padding = 0
		top_down_provider.name = "mock"
		top_down_provider.max_side_resolution_image = 640
		request_manager = RequestManager(
			user_info=self.user_info,
			quota_manager=self.quota_manager,
			map_entity=top_down_provider,
			log_manager=TestRequestManager.MockLogManager(),
			image_util=TestRequestManager.MockImageUtil(),
			geo_location_util=GeoLocationUtil(),
			resource_path=self.resource_path,
		)

		request_manager.make_request_for_block(
			centre_coordinates=(51.989954, 4.330746, 52.021186, 4.374115), zoom=14.0
		)

		given_arguments = top_down_provider.given_arguments["get_and_store_location"]
		self.assertEqual(given_arguments[0]["latitude"], 52.00686744205219)
		self.assertEqual(given_arguments[0]["longitude"], 4.358211820315531)
		self.assertEqual(given_arguments[8]["latitude"], 52.07447010004815)
		self.assertEqual(given_arguments[8]["longitude"], 4.468075101577653)
		self.assertEqual(given_arguments[72]["latitude"], 52.20936891128352)
		self.assertEqual(given_arguments[72]["longitude"], 4.6878016641018965)
		self.assertEqual(given_arguments[80]["latitude"], 52.27666518663308)
		self.assertEqual(given_arguments[80]["longitude"], 4.797664945364018)
