"""
Entry module of the application.
"""

from mesh_city.application import Application
from mesh_city.imagery_provider.request_manager import RequestManager
from mesh_city.imagery_provider.top_down_provider.google_maps_provider import GoogleMapsProvider
from mesh_city.logs.log_manager import LogManager
from mesh_city.user.quota_manager import QuotaManager
from mesh_city.user.user_info_handler import UserInfoHandler
from mesh_city.util.geo_location_util import GeoLocationUtil
from mesh_city.util.image_util import ImageUtil


def main() -> None:
	"""
	Entry function of the application.
	:return: Nothing.
	"""
	# Application()
	user_info_handler = UserInfoHandler()
	user_info = user_info_handler.load_user_info()
	quota_manager = QuotaManager(user_info)
	top_down_provider = GoogleMapsProvider(user_info, quota_manager)
	log_manager = LogManager()
	image_util = ImageUtil()
	geo_location_util = GeoLocationUtil()
	request_manager = RequestManager(user_info, quota_manager, top_down_provider, log_manager, image_util, geo_location_util)

	coordinates = (50, 5)
	# x_tile, y_tile = geo_location_util.degree_to_tile_value(49.99979502712741, 5.000152587890625, 20)
	# print(x_tile, y_tile)
	#
	# print(geo_location_util.tile_value_to_degree(538851, 355619, 20))
	# print(geo_location_util.tile_value_to_degree(538852, 355620, 20))

	# normalised_latitude, normalised_longitude = geo_location_util.normalise_coordinates(50, 5, 20)
	# x, y = geo_location_util.degree_to_tile_value(normalised_latitude, normalised_longitude, 20)
	# print(normalised_latitude, normalised_longitude)
	# print(x, y)
	#
	# top_latitude = geo_location_util.calc_next_location_latitude(normalised_latitude, normalised_longitude, 20, True)
	#
	# bottom_latitude1 = geo_location_util.calc_next_location_latitude(normalised_latitude, normalised_longitude, 20, False)
	# bottom_x1, bottom_y1 = geo_location_util.degree_to_tile_value(bottom_latitude1, normalised_longitude, 20)
	# bottom_latitude = geo_location_util.calc_next_location_latitude(bottom_latitude1, normalised_longitude, 20, False)
	# bottom_x, bottom_y = geo_location_util.degree_to_tile_value(bottom_latitude, normalised_longitude, 20)
	#
	# right_long = geo_location_util.calc_next_location_longitude(normalised_latitude, normalised_longitude, 20, True)
	# left_long = geo_location_util.calc_next_location_longitude(normalised_latitude, normalised_longitude, 20, False)
	#
	# print(top_latitude, bottom_latitude, right_long, left_long)
	#
	# top_x, top_y = geo_location_util.degree_to_tile_value(top_latitude, normalised_longitude, 20)
	# bottom_x, bottom_y = geo_location_util.degree_to_tile_value(bottom_latitude, normalised_longitude, 20)
	# right_x, right_y = geo_location_util.degree_to_tile_value(normalised_latitude, right_long, 20)
	# left_x, left_y = geo_location_util.degree_to_tile_value(normalised_latitude, left_long, 20)
	#
	# print(top_x, top_y)
	# print(bottom_x, bottom_y)
	# print(right_x, right_y)
	# print(left_x, left_y)

	# request_manager.make_single_request((normalised_latitude, normalised_longitude), 20)
	# request_manager.make_single_request((top_latitude, normalised_longitude), 20)
	# request_manager.make_single_request((bottom_latitude, normalised_longitude), 20)
	# request_manager.make_single_request((normalised_latitude, right_long), 20)
	# request_manager.make_single_request((normalised_latitude, left_long), 20)


	# grid_position = geo_location_util.degree_to_tile_value(90, 181, 20)
	# print(coordinates)
	# print(grid_position)
	#
	# normalised_coordinates1 = geo_location_util.normalise_coordinates(50, 5, 20)
	# print(normalised_coordinates1)
	#
	# normalised_coordinates = geo_location_util.tile_value_to_degree(grid_position[0], grid_position[1], 20)
	# normalised_grid_position = geo_location_util.degree_to_tile_value(normalised_coordinates[0], normalised_coordinates[1], 20)
	# print(normalised_coordinates)
	# print(normalised_grid_position)
	#
	# grid_position_plus1 = normalised_grid_position[0] + 2, normalised_grid_position[1]
	# coordinates_plus1 = geo_location_util.tile_value_to_degree(grid_position_plus1[0], grid_position_plus1[1], 20)
	# print(coordinates_plus1)
	# print(grid_position_plus1)
	#
	# request_manager.make_single_request(normalised_coordinates, 10)
	# request_manager.make_single_request(coordinates_plus1, 10)

	request_manager.make_request_two_coordinates(
		(51.913205, 4.453749), (51.912532, 4.456339), 20
	)
	# heemeraadseplein (51.913205, 4.453749), (51.912532, 4.456339)
	# whole of rotterdam (51.922922, 4.365737), (51.874373, 4.564900)
	# netherlands (51.912532, 4.456339), (51.912532, 4.456339)

if __name__ == '__main__':
	main()
