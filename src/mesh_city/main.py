from mesh_city.gui.application import Application
from mesh_city.imagery_provider.quota_manager import QuotaManager
from mesh_city.imagery_provider.request_manager import RequestManager
from mesh_city.imagery_provider.user_info_handler import UserInfoHandler


def main() -> None:

	# user_info_handler = UserInfoHandler()
	# user_info = user_info_handler.load_user_info()
	# quota_manager = QuotaManager(user_info)
	# request_manager = RequestManager(user_info=user_info, quota_manager=quota_manager)
	#
	# right = request_manager.calc_next_location_longitude(51.923539, 4.492560, 15, 640, True)
	# top = request_manager.calc_next_location_latitude(51.923539, 4.492560, 15, 640, True)

	# request_manager.make_single_request((51.923539, 4.492560), 15)
	# request_manager.make_single_request((51.923539, right), 15)
	# request_manager.make_single_request((top, 4.492560), 15)

	Application()

if __name__ == '__main__':
	main()
