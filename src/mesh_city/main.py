from mesh_city.gui.application import Application
from mesh_city.imagery_provider.request_manager import RequestManager
from mesh_city.user.quota_manager import QuotaManager
from mesh_city.user.user_info_handler import UserInfoHandler
from mesh_city.util.geo_location_util import GeoLocationUtil
from mesh_city.util.image_util import ImageUtil
from PIL import Image
from pathlib import Path




def main() -> None:

	user_info_handler = UserInfoHandler()
	user_info = user_info_handler.load_user_info()
	quota_manager = QuotaManager(user_info)
	request_manager = RequestManager(user_info=user_info, quota_manager=quota_manager)

	geo_location_util = GeoLocationUtil()

	# request_manager.make_request_for_block(centre_coordinates=[47.503353, 9.725559, 47.489911, 9.740647], zoom=request_manager.map_entity.max_zoom)

	right = geo_location_util.calc_next_location_longitude(51.923539, 4.492560, 15, 640, True)
	top = geo_location_util.calc_next_location_latitude(51.923539, 4.492560, 15, 640, True)
	# request_manager.make_single_request((51.923539, 4.492560), 15, 652, 628)

	# rio bottom:   -22.824637, -43.242729
	# rio top: -22.821384, -43.238813

	request_manager.get_area_coordinates(-22.824637, -43.242729, -22.821384, -43.238813, 20)

	# Application()

if __name__ == '__main__':
	main()
