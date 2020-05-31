"""
See :class:`.Application`
"""

from mesh_city.gui.main_screen import MainScreen
from mesh_city.imagery_provider.request_manager import RequestManager
from mesh_city.logs.log_manager import LogManager
from mesh_city.util.file_handler import FileHandler


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

	def late_init(self, user_entity):
		"""
		Initialises the fields that need the user information.
		"""
		self.user_entity = user_entity
		self.request_manager = RequestManager(user_entity=self.user_entity, application=self)

	def start(self):
		MainScreen(application=self)
