# pylint: disable=W0640
"""
A module containing the export window class
"""

from pathlib import Path
from tkinter import Button, Checkbutton, filedialog, IntVar, Label, Toplevel

from mesh_city.request.layers.buildings_layer import BuildingsLayer
from mesh_city.request.layers.cars_layer import CarsLayer
from mesh_city.request.layers.google_layer import GoogleLayer
from mesh_city.request.layers.trees_layer import TreesLayer
from mesh_city.request.scenario.scenario import Scenario


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

		self.image_path = self.application.file_handler.folder_overview['image_path']

		self.top_label = Label(self.top, text="Which request do you want to export?")
		self.top_label.grid(row=0)
		active_request_id = self.application.current_request.request_id
		temp_text = "Active Request: Request " + str(active_request_id)
		self.request_buttons = []
		self.request_buttons.append(
			Button(
			self.top,
			text=temp_text,
			width=20,
			height=3,
			command=lambda: self.load_request(self.application.current_request),
			bg="white"
			)
		)
		for (index, request) in enumerate(self.application.request_manager.requests):
			if request.request_id != active_request_id:
				self.request_buttons.append(
					Button(
					self.top,
					text="Request " + str(request.request_id),
					width=20,
					height=3,
					command=lambda: self.load_request(request),
					bg="white"
					)
				)
		for (index, request_button) in enumerate(self.request_buttons):
			request_button.grid(row=index + 1, column=0)

	def load_request(self, request):
		"""
		Loads the request. Then asks the user which features of this request to export
		:param name_directory: the directory where the request is stored
		:return: nothing (the window is updated to now show which features to export)
		"""
		for button in self.request_buttons:
			button.grid_forget()
		self.top_label.forget()

		self.application.set_current_request(request=request)
		self.top_label.configure(text="What do you want to export?")

		self.int_variable_list_layers = []
		next_start = 0
		for (index, layer) in enumerate(request.layers):
			self.int_variable_list_layers.append(IntVar())
			text = ""
			if isinstance(layer, GoogleLayer):
				text = "Google Imagery"
			elif isinstance(layer, TreesLayer):
				text = "Tree detections CSV"
			elif isinstance(layer, CarsLayer):
				text = "Car detections CSV"
			elif isinstance(layer, BuildingsLayer):
				text = "Building detections GeoJSON"
			Checkbutton(self.top, text=text,
				variable=self.int_variable_list_layers[index]).grid(row=index + 1)
			next_start = index + 1

		self.int_variable_list_scenarios = []
		for (index, scenario) in enumerate(request.scenarios.values()):
			self.int_variable_list_scenarios.append(IntVar())
			text = ""
			if isinstance(scenario, Scenario):
				text = "Scenario: " + scenario.scenario_name
			text = scenario.scenario_name
			Checkbutton(self.top, text=text,
				variable=self.int_variable_list_scenarios[index]).grid(row=next_start + 1)
			next_start += 1

		Button(self.top, text="Confirm", command=lambda: self.cleanup(request),
			bg="white").grid(row=next_start)

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

		has_export_scenario = False
		scenario_mask = []
		for element in self.int_variable_list_scenarios:
			if element.get() == 1:
				has_export_scenario = True
			scenario_mask.append(element.get() == 1)

		if has_export_scenario or has_export_scenario:
			export_directory = Path(filedialog.askdirectory())
			if has_export_layer:
				self.application.export_request_layers(
					request=request, layer_mask=layer_mask, export_directory=export_directory
				)
			if has_export_scenario:
				None

		self.top.destroy()
