"""
See :class:`.Application`
"""

from pathlib import Path
from typing import List, Sequence, Union

from PIL import Image

from mesh_city.detection.detection_pipeline import DetectionPipeline, DetectionType
from mesh_city.detection.information_string_builder import InformationStringBuilder
from mesh_city.gui.main_screen import MainScreen
from mesh_city.gui.request_renderer import RequestRenderer
from mesh_city.logs.log_manager import LogManager
from mesh_city.request.entities.request import Request
from mesh_city.request.layers.layer import Layer
from mesh_city.request.request_exporter import RequestExporter
from mesh_city.request.request_maker import RequestMaker
from mesh_city.request.request_manager import RequestManager
from mesh_city.request.request_observer import RequestObserver
from mesh_city.scenario.scenario import Scenario
from mesh_city.scenario.scenario_pipeline import ScenarioPipeline
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
		self.current_request = None
		self.request_manager = self.get_request_manager()
		self.request_observer = None
		self.main_screen = None

	def get_main_screen(self) -> MainScreen:
		"""
		Gets the MainScreen instance of this Application
		:return: The MainScreen instance
		"""
		return self.main_screen

	def get_request_manager(self) -> RequestManager:
		"""
		Creates a RequestManager instance and makes it load both previous requests and references to downloaded
		imagery.

		:return: The RequestManager instance with requests and grid loaded from disk.
		"""

		request_manager = RequestManager(self.file_handler.folder_overview["image_path"])
		request_manager.load_data()
		return request_manager

	def set_user_entity(self, user_entity):
		"""
		Initialises the fields that need the user information.
		"""

		self.user_entity = user_entity
		self.request_maker = RequestMaker(request_manager=self.request_manager)

	def run_detection(self, request: Request, to_detect: Sequence[DetectionType]) -> None:
		"""
		Runs a detection based on the current request information and the layers that have to be
		detected.

		:param request: The request to run detections for
		:param to_detect: The detections to run
		:return: None
		"""

		pipeline = DetectionPipeline(self.file_handler, self.request_manager, to_detect)
		new_layers = pipeline.process(request)
		for new_layer in new_layers:
			self.current_request.add_layer(new_layer)

	def create_scenario(self, request: RequestManager, scenarios_to_create, name=None):
		"""
		Creates a scenario based on a request
		:param request: A Request
		:param scenarios_to_create: A para
		:param name:
		:return:
		"""
		pipeline = ScenarioPipeline(
			request_manager=self.request_manager, scenarios_to_create=scenarios_to_create, name=name
		)
		new_scenario = pipeline.process(request)
		self.current_request.add_scenario(new_scenario)

		self.load_scenario_onscreen(name=new_scenario.scenario_name)

	def make_location_request(self, latitude: float, longitude: float, name: str = None) -> None:
		"""
		Makes a location request and updates the application correspondingly.

		:param latitude: The latitude of the request
		:param longitude: The longitude of the request
		:return: None
		"""
		self.request_observer = RequestObserver(self.main_screen.master)
		self.request_maker.attach_observer(self.request_observer)

		finished_request = self.request_maker.make_location_request(
			latitude=latitude, longitude=longitude, name=name
		)

		self.request_maker.detach_observer(self.request_observer)

		self.process_finished_request(request=finished_request)

		self.log_manager.write_log(self.user_entity)

	def make_area_request(
		self,
		bottom_latitude: float,
		left_longitude: float,
		top_latitude: float,
		right_longitude: float,
		name: str = None
	) -> None:
		"""
		Makes an area request and updates the application correspondingly.

		:param bottom_latitude: The bottom-most latitude value
		:param left_longitude: The leftmost longitude value
		:param top_latitude: The top-most latitude value
		:param right_longitude: The rightmost longitude value
		:return: None
		"""
		self.request_observer = RequestObserver(self.main_screen.master)
		self.request_maker.attach_observer(self.request_observer)

		finished_request = self.request_maker.make_area_request(
			bottom_latitude=bottom_latitude,
			left_longitude=left_longitude,
			top_latitude=top_latitude,
			right_longitude=right_longitude,
			name=name
		)

		self.request_maker.detach_observer(self.request_observer)

		self.process_finished_request(request=finished_request)

		self.log_manager.write_log(self.user_entity)

	def set_current_request(self, request: Request) -> None:
		"""
		Sets the current request to a new Request and updates the view accordingly.

		:param request:
		:return:
		"""
		self.current_request = request
		self.load_request_onscreen(request)
		self.main_screen.active_layers = ["Google Maps"]

	def load_request_specific_layers(self, request: Request, layer_mask: List[bool]) -> None:
		"""
		Loads specific layers of a request onto the screen.

		:param request: The request to load
		:param layer_mask: A boolean mask representing which layers to render.
		:return: None
		"""

		canvas_image = RequestRenderer.render_request(request=request, layer_mask=layer_mask)
		self.main_screen.set_canvas_image(canvas_image)

		layer_list = []
		for (index, element) in enumerate(layer_mask):
			if element is True:
				layer_list.append(self.current_request.layers[index])
		text_to_show = self.get_statistics(element_list=layer_list)
		self.main_screen.update_text(text_to_show)

	def export_request_layers(
		self, request: Request, layer_mask: List[bool], export_directory: Path
	) -> None:
		"""
		Export a set of layers from a Request.

		:param request: The request to export
		:param layer_mask: A boolean mask representing which layers to export.
		:param export_directory: A path to the root of where the layers should be exported to.
		:return: None
		"""

		request_exporter = RequestExporter(request_manager=self.request_manager)
		request_exporter.export_request_layers(
			request=request, layer_mask=layer_mask, export_directory=export_directory
		)

	def export_request_scenarios(
		self, scenario_list: Sequence[Scenario], export_directory: Path
	) -> None:
		"""
		Exports scenario's certain requests belonging to a request to an export directory.
		:param request: The request to export scenarios for
		:param scenario_list: Which scenario's to export
		:param export_directory: The directory to export scenario's to
		:return:
		"""

		request_exporter = RequestExporter(request_manager=self.request_manager)
		request_exporter.export_request_scenarios(
			scenario_list=scenario_list, export_directory=export_directory
		)

	def load_request_onscreen(self, request: Request) -> None:
		"""
		Loads a request on screen.

		:param request: The request to load on screen.
		:return: None
		"""
		canvas_image = RequestRenderer.create_image_from_layer(request=request, layer_index=0)
		self.main_screen.set_canvas_image(canvas_image)
		self.main_screen.delete_text()

	def load_scenario_onscreen(self, name: str) -> None:
		"""
		Loads a named scenario of the current request
		:param name: The name of a scenario of the current request.
		:return: None
		"""
		canvas_image = Image.open(self.current_request.scenarios[name].scenario_path)
		self.main_screen.set_gif(canvas_image)

		text_to_show = self.get_statistics(element_list=[self.current_request.scenarios[name]])
		self.main_screen.update_text(text_to_show)

	def process_finished_request(self, request: Request) -> None:
		"""
		Adds a made request to the RequestManager of the Application sets the state of the Application
		accordingly with the made request becoming the current request.

		:param request: The request that was made
		:return: None
		"""

		self.request_manager.add_request(request)
		self.request_manager.serialize_requests()
		self.set_current_request(request=request)

	def get_statistics(self, element_list: Sequence[Union[Layer, Scenario]]):
		"""
		Method which can be called to count, analyse and create some statistics of the detections
		saved in layers of the active request.
		:return:
		"""
		bio_path = self.file_handler.folder_overview['biome_index']
		info_gen = InformationStringBuilder(bio_path)

		return info_gen.process(element_list=element_list)

	def start(self):
		"""
		Creates a mainscreen UI element and passes self as application context.

		:return: None
		"""

		self.main_screen = MainScreen(application=self)
		self.main_screen.run()
