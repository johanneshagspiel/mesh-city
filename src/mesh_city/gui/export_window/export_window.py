# pylint: disable=W0640
"""
A module containing the export window class
"""

from pathlib import Path
from tkinter import CENTER, Checkbutton, filedialog, IntVar, Label, Toplevel, W

from mesh_city.gui.widgets.button import Button as CButton
from mesh_city.gui.widgets.container import Container
from mesh_city.gui.widgets.scrollable_container import ScrollableContainer
from mesh_city.gui.widgets.widget_geometry import WidgetGeometry
from mesh_city.request.layers.buildings_layer import BuildingsLayer
from mesh_city.request.layers.cars_layer import CarsLayer
from mesh_city.request.layers.image_layer import ImageLayer
from mesh_city.request.layers.trees_layer import TreesLayer


class ExportWindow:
	"""
	The window where the user can select what they want to export as well as where to export that to
	"""

	def __init__(self, master, application, main_screen):
		"""
		First asks the user which request to export
		:param master: the master tkinter application
		:param application: the global application context
		"""
		self.master = master
		self.value = ""
		self.application = application
		self.main_screen = main_screen

		self.top = Toplevel(master)
		self.top.config(padx=4)
		self.top.config(pady=4)
		self.top.grab_set()

		self.image_path = self.application.file_handler.folder_overview['image_path']

		self.top.geometry("%dx%d+%d+%d" % (490, 270, 0, 0))
		self.layer_label_style = {
			"font": ("Eurostile LT Std", 18), "background": "white", "anchor": W
		}

		self.content = Container(WidgetGeometry(480, 260, 0, 0), self.top, background="white")

		self.top_label = Label(
			self.content,
			text="Which request do you want to export?",
			**self.layer_label_style,
			justify=CENTER
		)
		self.top_label.place(width=460, height=40, x=10, y=0)

		self.scrollable_content = ScrollableContainer(
			WidgetGeometry(470, 200, 0, 50), self.content, background="white"
		)

		active_request_id = self.application.current_request.request_id
		temp_text = "Active Request: " + self.application.current_request.name
		self.request_buttons = []

		self.request_buttons.append(
			self.scrollable_content.add_row(
			lambda parent: CButton(
			WidgetGeometry(400, 50, 20, 0),
			temp_text,
			lambda _: self.load_request(self.application.current_request),
			parent
			)
			)
		)

		if self.application.current_scenario is not None:
			self.request_buttons.append(
				self.scrollable_content.add_row(
				lambda parent: CButton(
				WidgetGeometry(400, 50, 20, 0),
				"Current scenario",
				lambda _: self.export_scenario(),
				parent
				)
				)
			)

		for request in self.application.request_manager.requests:
			if request.request_id != active_request_id:
				self.request_buttons.append(
					self.scrollable_content.add_row(
					lambda parent: CButton(
					WidgetGeometry(400, 50, 20, 0),
					request.name,
					lambda _: self.load_request(request),
					parent
					)
					)
				)

	def export_scenario(self):
		"""
		Temporary callback for exporting the current scenario of the application
		:return: None
		"""
		export_directory = Path(filedialog.askdirectory())
		self.application.export_scenario(
			scenario=self.application.current_scenario, export_directory=export_directory
		)
		self.top.destroy()

	def load_request(self, request):
		"""
		Loads the request. Then asks the user which features of this request to export
		:param name_directory: the directory where the request is stored
		:return: nothing (the window is updated to now show which features to export)
		"""
		self.scrollable_content.place_forget()

		self.application.set_current_request(request=request)
		self.top_label.configure(text="What do you want to export?")

		self.int_variable_list_layers = []

		index = 40
		for (position, layer) in enumerate(request.layers):
			self.int_variable_list_layers.append(IntVar())
			text = ""
			if isinstance(layer, ImageLayer):
				text = "Google Imagery"
			elif isinstance(layer, TreesLayer):
				text = "Tree detections CSV"
			elif isinstance(layer, CarsLayer):
				text = "Car detections CSV"
			elif isinstance(layer, BuildingsLayer):
				text = "Building detections GeoJSON"
			temp_button = Checkbutton(
				self.content,
				text=text,
				**self.layer_label_style,
				variable=self.int_variable_list_layers[position]
			)
			temp_button.place(width=460, height=40, x=10, y=index)
			index += 40

		CButton(
			WidgetGeometry(300, 50, 75, index), "Confirm", lambda _: self.cleanup(request), self.top
		)

	def cleanup(self, request):
		"""
		Asks the user to select a folder to export to. Then copies all the files into this folder
		:return: nothing (the desired images are exported to a folder)
		"""
		has_export_layer = False
		layer_mask = []
		for element in self.int_variable_list_layers:
			if element.get() == 1:
				has_export_layer = True
			layer_mask.append(element.get() == 1)

		if has_export_layer:
			export_directory = Path(filedialog.askdirectory())
			if has_export_layer:
				self.application.export_request_layers(
					request=request, layer_mask=layer_mask, export_directory=export_directory
				)

		self.top.grab_release()
		self.top.destroy()
