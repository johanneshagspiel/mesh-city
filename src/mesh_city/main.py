from mesh_city.application import Application
from mesh_city.imagery_provider.request_manager import RequestManager
from mesh_city.imagery_provider.top_down_provider.ahn_provider import AhnProvider
from mesh_city.user.quota_manager import QuotaManager
from mesh_city.user.user_info_handler import UserInfoHandler


def main() -> None:

	user_info_handler = UserInfoHandler()
	user_info = user_info_handler.load_user_info()
	quota_manager = QuotaManager(user_info)
	request_manager = RequestManager(user_info=user_info, quota_manager=quota_manager)

	#test = AhnProvider(user_info, quota_manager)
	#test.get_height_from_pixel(950, 960)
	#test.store_to_json()

	#print(request_manager.calculate_centre_coordinates_two_coordinate_input([51, 4.2], [51.1, 4.3], 20)[0])

	request_manager.make_request_for_block(
		centre_coordinates=[51.997004, 4.370530, 52.001486, 4.376918],
		zoom=request_manager.map_entity.max_zoom
	)
	# right = request_manager.calc_next_location_longitude(51.923539, 4.492560, 15, 640, True)
	# top = request_manager.calc_next_location_latitude(51.923539, 4.492560, 15, 640, True)

	# request_manager.make_single_request((51.923539, 4.492560), 15)
	# request_manager.make_single_request((51.923539, right), 15)
	# request_manager.make_single_request((top, 4.492560), 15)

	#Application()


if __name__ == '__main__':
	main()
