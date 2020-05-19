"""
See :class:`.Application`
"""

from mesh_city.gui.main_screen import MainScreen
from mesh_city.imagery_provider.request_manager import RequestManager
from mesh_city.user.quota_manager import QuotaManager
from mesh_city.user.user_info_handler import UserInfoHandler


class Application:
	"""
	For the application to work, you will need to have
	``resources/images/request_0/0_tile_0_0/concat_image_request_10_tile_0_0.png``
	"""

	def __init__(self):
		self.user_info_handler = UserInfoHandler()
		self.quota_manager = None
		self.request_manager = None
		self.user_info = None

		MainScreen(application=self)

	def late_init(self):
		"""
		Initialises the fields that need the user information.
		"""

		self.user_info_handler.store_user_info(self.user_info)
		self.quota_manager = QuotaManager(self.user_info)
		self.request_manager = RequestManager(self.user_info, self.quota_manager)
