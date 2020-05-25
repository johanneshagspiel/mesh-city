"""
See :class:`.Application`
"""

from mesh_city.gui.main_screen import MainScreen
from mesh_city.imagery_provider.request_manager import RequestManager
from mesh_city.logs.log_manager import LogManager
from mesh_city.util.file_handler import FileHandler
from mesh_city.util.geo_location_util import GeoLocationUtil
from mesh_city.util.image_util import ImageUtil


class Application:
	"""
	For the application to work, you will need to have
	``resources/images/request_0/0_tile_0_0/concat_image_request_10_tile_0_0.png``
	"""

	def __init__(self):
		self.file_handler = FileHandler()
		self.log_manager = LogManager(file_handler=self.file_handler)
		self.request_manager = None
		self.user_entity = None

		MainScreen(application=self)

	def late_init(self, user_entity):
		"""
		Initialises the fields that need the user information.
		"""
		self.user_entity = user_entity
		self.request_manager = RequestManager(
			file_handler=self.file_handler,
			log_manager=self.log_manager,
			image_util=ImageUtil(),
			geo_location_util=GeoLocationUtil(),
		)
