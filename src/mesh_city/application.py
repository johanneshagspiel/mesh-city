"""
See :class:`.Application`
"""
from tkinter import END

from mesh_city.detection.pipeline import Pipeline
from mesh_city.gui.main_screen import MainScreen
from mesh_city.imagery_provider.request_maker import RequestMaker
from mesh_city.imagery_provider.request_manager import RequestManager
from mesh_city.logs.log_manager import LogManager
from mesh_city.request.google_layer import GoogleLayer
from mesh_city.util.file_handler import FileHandler


class Application:
	"""
	For the application to work, you will need to have
	``resources/images/request_0/0_tile_0_0/concat_image_request_10_tile_0_0.png``
	"""

	def __init__(self):
		self.file_handler = FileHandler()
		self.log_manager = LogManager(file_handler=self.file_handler)
		self.request_maker = None
		self.user_entity = None
		self.main_screen = None
		self.request_manager = self.get_request_manager()

	def get_request_manager(self):
		return RequestManager(self.file_handler)

	def late_init(self, user_entity):
		"""
		Initialises the fields that need the user information.
		"""
		self.user_entity = user_entity
		self.request_maker = RequestMaker(
			user_entity=self.user_entity, application=self, request_manager=self.request_manager
		)

	def run_detection(self, building_instructions, to_detect):
		"""
		Runs a detection based on the current request information and the layers that have to be
		detected.
		:param building_instructions:
		:param to_detect:
		:return:
		"""
		Pipeline(self, to_detect, building_instructions).push_forward()
		self.main_screen.active_layers = to_detect
		self.main_screen.set_canvas_image()
		self.main_screen.update_text()

	def make_location_request(self, latitude, longitude):
		finished_request = self.request_maker.make_location_request(latitude=latitude, longitude=longitude)
		self.process_finished_request(request=finished_request)


	def make_area_request(self, bottom_latitude, left_longitude, top_latitude, right_longitude):
		finished_request = self.request_maker.make_area_request(
			bottom_latitude=bottom_latitude,
			left_longitude=left_longitude,
			top_latitude=top_latitude,
			right_longitude=right_longitude
		)
		self.process_finished_request(request=finished_request)

	def print_request_info(self,request):
		if request.has_layer_of_type(GoogleLayer):
			google_layer = request.get_layer_of_type(GoogleLayer)
			for (index,tile) in enumerate(google_layer.tiles):
				print(str(index)+": "+str(tile.path))
	def process_finished_request(self,request):

		self.request_manager.add_request(request)
		self.print_request_info(request)
		# self.main_screen.set_canvas_image()
		# self.main_screen.information_general.configure(state='normal')
		# self.main_screen.information_general.delete('1.0', END)
		# self.main_screen.information_general.insert(END, "General")
		# self.main_screen.information_general.configure(state='disabled')
	def start(self):
		"""
		Creates a mainscreen UI element and passes self as application context.
		:return: None
		"""
		self.main_screen = MainScreen(application=self)
		self.main_screen.run()
