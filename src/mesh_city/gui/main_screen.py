"""
See :class:`.MainScreen`
"""

from pathlib import Path
from tkinter import DISABLED, END, Label, mainloop, NORMAL, Text, Tk, W, WORD
from typing import List, Optional, Union

from PIL import Image

from mesh_city.detection.detection_pipeline import DetectionType
from mesh_city.gui.detection_window.detection_window import DetectionWindow
from mesh_city.gui.eco_window.eco_window import EcoWindow
from mesh_city.gui.export_window.export_window import ExportWindow
from mesh_city.gui.layers_window.layers_window import LayersWindow
from mesh_city.gui.load_font import load_font
from mesh_city.gui.load_window.load_window import LoadWindow
from mesh_city.gui.load_window.select_load_option import SelectLoadOption
from mesh_city.gui.mainscreen_image.canvas_image import CanvasImage
from mesh_city.gui.mainscreen_image.gif_image import GifImage
from mesh_city.gui.search_window.search_window_start import SearchWindowStart
from mesh_city.gui.tutorial_window.tutorial_window import TutorialWindow
from mesh_city.gui.user_window.user_window import UserWindow
from mesh_city.gui.widgets.button import Button as CButton
from mesh_city.gui.widgets.container import Container
from mesh_city.gui.widgets.layer_button import LayerButton
from mesh_city.gui.widgets.widget_geometry import WidgetGeometry
from mesh_city.request.layers.buildings_layer import BuildingsLayer
from mesh_city.request.layers.cars_layer import CarsLayer
from mesh_city.request.layers.image_layer import ImageLayer
from mesh_city.request.layers.trees_layer import TreesLayer


class MainScreen:
	"""
	The main screen of the application where the map is shown as well as as all the function one
	can do on the map such as loading requests or looking at different layers
	"""

	def __init__(self, application) -> None:
		"""
		Setting up the main screen
		:param application: the global application context
		"""

		self.application = application
		self.master = Tk()

		self.master.title("Planet Painter")
		self.master.geometry("%dx%d+%d+%d" % (1600, 900, 160, 56))
		self.master.resizable(width=False, height=False)
		self.master.iconbitmap(True, self.application.file_handler.folder_overview["icon"])

		for file in self.application.file_handler.folder_overview["fonts"].glob("*"):
			load_font(file)

		users = self.application.log_manager.read_log(
			path=self.application.file_handler.folder_overview["users.json"],
			type_document="users.json",
		)
		self.application.set_user_entity(users["John"])

		self.active_layers: List[str] = []

		self.content = Container(WidgetGeometry(1600, 900, 0, 0), self.master, background="black")

		self.canvas_image: Optional[CanvasImage] = None
		logo_path: Path = self.application.file_handler.folder_overview["logo"]
		self.set_canvas_image(Image.open(logo_path))

		self.left_container = Container(WidgetGeometry(350, 900, 0, 0), self.content)
		self.right_container = Container(WidgetGeometry(350, 900, 1250, 0), self.content)

		CButton(
			WidgetGeometry(200, 50, 75, 50),
			"search",
			lambda _: self.search_window(),
			self.left_container,
		)
		CButton(
			WidgetGeometry(200, 50, 75, 120),
			"load",
			lambda _: self.load_window(),
			self.left_container,
		)
		CButton(
			WidgetGeometry(200, 50, 75, 380),
			"scenarios",
			lambda _: self.eco_window(),
			self.left_container,
		)
		CButton(
			WidgetGeometry(200, 50, 75, 480),
			"export",
			lambda _: self.export_window(),
			self.left_container,
		)

		CButton(
			WidgetGeometry(200, 50, 75, 580),
			"user",
			lambda _: self.user_window(),
			self.left_container,
		)

		self.layers_container = Container(
			WidgetGeometry(250, 140, 50, 220), master=self.left_container, background="white",
		)
		layer_label_style = {"font": ("Eurostile LT Std", 18), "background": "white", "anchor": W}
		Label(self.layers_container, text="trees", **layer_label_style,
				).place(width=100, height=40, x=0, y=0)
		Label(self.layers_container, text="buildings", **layer_label_style,
				).place(width=100, height=40, x=0, y=50)
		Label(self.layers_container, text="cars", **layer_label_style,
				).place(width=100, height=40, x=0, y=100)

		self.information_general = Text(self.right_container, wrap=WORD, borderwidth=0)
		self.information_general.configure(font=("Eurostile LT Std", 12))
		self.information_general.insert(END, "")
		self.information_general.configure(state=DISABLED)
		self.information_general.bind("<Double-1>", lambda event: "break")
		self.information_general.bind("<Button-1>", lambda event: "break")
		self.information_general.config(cursor="")
		self.information_general.place(width=250, height=750, x=50, y=50)

		self.gif_image: Optional[GifImage] = None
		self.trees_detect_button: Optional[LayerButton] = None
		self.buildings_detect_button: Optional[LayerButton] = None
		self.cars_detect_button: Optional[LayerButton] = None
		self.trees_layer_button: Optional[LayerButton] = None
		self.buildings_layer_button: Optional[LayerButton] = None
		self.cars_layer_button: Optional[LayerButton] = None

	def run(self) -> None:
		"""
		Runs the main loop that updates the GUI and processes user input.
		:return: None
		"""

		start_up_window = self.start_up()
		self.master.wait_window(start_up_window.top)

		self.render_dynamic_widgets()

		mainloop()

	def render_dynamic_widgets(self) -> None:
		"""
		Updates dynamic widgets to reflect events such as new features being detected.
		:return: None
		"""
		if self.trees_detect_button is not None:
			self.trees_detect_button.destroy()
			self.trees_detect_button = None
		if not self.application.current_request.has_layer_of_type(TreesLayer):
			self.trees_detect_button = CButton(
				WidgetGeometry(100, 40, 150, 0),
				text="detect",
				on_click=lambda _: self._run_detection(DetectionType.TREES),
				master=self.layers_container,
			)

		# Buildings detect button logic
		if self.buildings_detect_button is not None:
			self.buildings_detect_button.destroy()
			self.buildings_detect_button = None
		if not self.application.current_request.has_layer_of_type(BuildingsLayer):
			self.buildings_detect_button = CButton(
				WidgetGeometry(100, 40, 150, 50),
				text="detect",
				on_click=lambda _: self._run_detection(DetectionType.BUILDINGS),
				master=self.layers_container,
			)

		# Cars detect button logic
		if self.cars_detect_button is not None:
			self.cars_detect_button.destroy()
			self.cars_detect_button = None
		if not self.application.current_request.has_layer_of_type(CarsLayer):
			self.cars_detect_button = CButton(
				WidgetGeometry(100, 40, 150, 100),
				text="detect",
				on_click=lambda _: self._run_detection(DetectionType.CARS),
				master=self.layers_container,
			)

		# Trees layer button logic
		if self.trees_layer_button is not None:
			self.trees_layer_button.destroy()
			self.trees_layer_button = None
		if self.application.current_request.has_layer_of_type(TreesLayer):
			trees_layer_active = "Trees" in self.active_layers
			self.trees_layer_button = LayerButton(
				WidgetGeometry(80, 40, 170, 0),
				text="on" if trees_layer_active else "off",
				button_color="green" if trees_layer_active else "#EEEEEE",
				text_color="white" if trees_layer_active else "black",
				on_click=lambda _: self._set_layer_visibility("Trees", not trees_layer_active),
				master=self.layers_container,
			)

		# Buildings layer button logic
		if self.buildings_layer_button is not None:
			self.buildings_layer_button.destroy()
			self.buildings_layer_button = None
		if self.application.current_request.has_layer_of_type(BuildingsLayer):
			buildings_layer_active = "Buildings" in self.active_layers
			self.buildings_layer_button = LayerButton(
				WidgetGeometry(80, 40, 170, 50),
				text="on" if buildings_layer_active else "off",
				button_color="red" if buildings_layer_active else "#EEEEEE",
				text_color="white" if buildings_layer_active else "black",
				on_click=lambda _: self._set_layer_visibility("Buildings", not buildings_layer_active),
				master=self.layers_container,
			)

		# Cars layer button logic
		if self.cars_layer_button is not None:
			self.cars_layer_button.destroy()
			self.cars_layer_button = None
		if self.application.current_request.has_layer_of_type(CarsLayer):
			cars_layer_active = "Cars" in self.active_layers
			self.cars_layer_button = LayerButton(
				WidgetGeometry(80, 40, 170, 100),
				text="on" if cars_layer_active else "off",
				button_color="blue" if cars_layer_active else "#EEEEEE",
				text_color="white" if cars_layer_active else "black",
				on_click=lambda _: self._set_layer_visibility("Cars", not cars_layer_active),
				master=self.layers_container,
			)

	def _run_detection(self, detection_type: DetectionType) -> None:
		"""
		Forwards a detection event to the application and updates the dynamic widgets after this
		has finished.
		:param detection_type: The type of detection to run
		:return: None
		"""
		self.application.run_detection(
			request=self.application.current_request, to_detect=[detection_type],
		)
		self.render_dynamic_widgets()

	def _load_layers(self) -> None:
		detected_layers: List[str] = []
		for layer in self.application.current_request.layers:
			if isinstance(layer, ImageLayer):
				detected_layers.append("Google Maps")
			if isinstance(layer, TreesLayer):
				detected_layers.append("Trees")
			if isinstance(layer, CarsLayer):
				detected_layers.append("Cars")
			if isinstance(layer, BuildingsLayer):
				detected_layers.append("Buildings")

		layer_mask: List[bool] = [(layer in self.active_layers) for layer in detected_layers]
		self.application.load_request_specific_layers(
			request=self.application.current_request, layer_mask=layer_mask,
		)

		self.render_dynamic_widgets()

	def _set_layer_visibility(self, layer: str, layer_visible: bool) -> None:
		if layer_visible and layer not in self.active_layers:
			self.active_layers.append(layer)
		elif not layer_visible and layer in self.active_layers:
			self.active_layers.remove(layer)

		self._load_layers()

	def export_window(self) -> None:
		"""
		Creates an export window
		:return: None
		"""
		ExportWindow(master=self.master, application=self.application, main_screen=self)

	def layers_window(self) -> None:
		"""
		Creates a layers window object
		:return: None
		"""
		LayersWindow(self.master, self.application, self)

	def load_window(self) -> None:
		"""
		Creates a load request window object
		:return: None
		"""
		SelectLoadOption(self.master, self.application, self)

	def search_window(self) -> None:
		"""
		Creates a search window object
		:return: None
		"""
		SearchWindowStart(self.master, self.application, self)

	def detect_window(self) -> None:
		"""
		Creates a detect window object
		:return: None
		"""
		DetectionWindow(self.master, self.application)

	def user_window(self) -> None:
		"""
		Creates a UserWindow object
		:return: None
		"""
		UserWindow(master=self.master, application=self.application, main_screen=self)

	def eco_window(self) -> None:
		"""
		Creates an EcoWindow object
		:return: None
		"""
		EcoWindow(master=self.master, application=self.application, main_screen=self)

	def set_canvas_image(self, image: Image) -> None:
		"""
		Calls methods needed to updates the image seen on the map
		:return: Nothing
		"""
		if self.canvas_image is not None:
			self.canvas_image.destroy()
		self.canvas_image = CanvasImage(self.content, image)

	def set_gif(self, image) -> None:
		"""
		Places a gif image on the main screen.
		:param image:
		:return:
		"""
		self.gif_image = GifImage(self.master)
		self.gif_image.load(image)
		# TODO: Position and size this one correctly
		self.gif_image.place(width=900, height=900, x=350, y=0)

	def delete_text(self):
		"""
		Method to delete all text in the right hand side general information text field
		:return: None
		"""
		self.information_general.configure(state=NORMAL)
		self.information_general.delete("1.0", END)
		self.information_general.insert(END, "")
		self.information_general.configure(state=DISABLED)

	def update_text(self, text_to_show: str) -> None:
		"""
		Method to update the text field on the main screen
		:return: None
		"""
		self.information_general.configure(state=NORMAL)
		self.information_general.delete("1.0", END)
		self.information_general.insert(END, text_to_show)
		self.information_general.configure(state=DISABLED)

	def start_up(self) -> Union[TutorialWindow, LoadWindow]:
		"""
		Method called when starting the application. Creates either tutorial window or load screen
		:return: None
		"""
		if len(self.application.request_manager.requests) == 0:
			return TutorialWindow(self.master, self.application, self)

		return LoadWindow(self.master, self.application, self)
