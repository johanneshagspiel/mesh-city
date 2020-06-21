"""
The module containing the eco window
"""
import math
from tkinter import Entry, Label, Scale, Toplevel, W

import geopandas as gpd
import pandas as pd

from mesh_city.gui.widgets.button import Button as CButton
from mesh_city.gui.widgets.container import Container
from mesh_city.gui.widgets.widget_geometry import WidgetGeometry
from mesh_city.request.layers.buildings_layer import BuildingsLayer
from mesh_city.request.layers.cars_layer import CarsLayer
from mesh_city.request.layers.google_layer import ImageLayer
from mesh_city.request.layers.trees_layer import TreesLayer
from mesh_city.scenario.scenario_pipeline import ScenarioModificationType


class EcoWindow:
	"""
	Window showing all the options what the user can do to increase the number of trees in an area.
	"""

	def __init__(self, master, application, main_screen):
		"""
		The initialization method
		:param master: the master tkinter object
		:param application: the global application context
		:param main_screen: the main_screen of the application
		"""
		self.main_screen = main_screen
		self.master = master
		self.value = ""
		self.application = application
		self.top = Toplevel(master)

		self.top.config(padx=4)
		self.top.config(pady=4)

		self.cars_enabled = True
		self.buildings_enabled = True

		detected_layers = []
		for layer in self.application.current_request.layers:
			if isinstance(layer, ImageLayer):
				detected_layers.append("Google Maps")
			if isinstance(layer, TreesLayer):
				detected_layers.append("Trees")
			if isinstance(layer, CarsLayer):
				detected_layers.append("Cars")
			if isinstance(layer, BuildingsLayer):
				detected_layers.append("Buildings")

		self.top.grab_set()

		self.top.geometry("%dx%d+%d+%d" % (900, 510, 0, 0))
		self.layer_label_style = {
			"font": ("Eurostile LT Std", 18), "background": "white", "anchor": W
		}
		self.scale_style = {"font": ("Eurostile LT Std", 18), "background": "white"}

		self.content = Container(WidgetGeometry(890, 500, 0, 0), self.top, background="white")

		self.top_label = Label(self.content, text="", **self.layer_label_style)
		self.top_label["anchor"] = "center"
		self.top_label.place(width=890, height=40, x=0, y=0)

		self.usable_layer = []

		if "Trees" in detected_layers:
			self.tree_layer_panda = pd.read_csv(
				self.application.current_request.get_layer_of_type(TreesLayer).detections_path
			)
			if self.tree_layer_panda.shape[0] > 1:
				self.usable_layer.append("Trees")
		if "Cars" in detected_layers:
			self.car_layer_panda = pd.read_csv(
				self.application.current_request.get_layer_of_type(CarsLayer).detections_path
			)
			if self.car_layer_panda.shape[0] > 1:
				self.usable_layer.append("Cars")
				self.max_amount_cars_swapable = self.car_layer_panda.shape[0] - 1
		if "Buildings" in detected_layers:
			self.buildings_gdf = gpd.read_file(
				self.application.current_request.get_layer_of_type(BuildingsLayer).detections_path
			)
			if self.buildings_gdf.shape[0] > 1:
				self.usable_layer.append("Buildings")
				self.max_amount_buildings_coverable = self.buildings_gdf.shape[0]

		if "Trees" in self.usable_layer or "Buildings" in self.usable_layer:
			self.top_label["text"] = "Scenario Creator"

			self.step_counter = 1
			self.to_forget = []
			self.important_widgets = []
			self.modification_list = []

			self.step_one_text_label = Label(self.content, text="Step 1", **self.layer_label_style)
			self.step_one_text_label.place(width=80, height=40, x=10, y=40)

			secondary_label_text = "How do you want to increase the number of plants in this area?"
			self.secondary_label = Label(
				self.content, text=secondary_label_text, **self.layer_label_style
			)
			self.secondary_label.place(width=800, height=40, x=110, y=40)

			counter = 10
			if "Trees" in self.usable_layer:
				self.increase_amount_button = CButton(
					WidgetGeometry(270, 50, counter, 80),
					"Add more Trees",
					lambda _: self.add_more_trees(),
					self.content,
				)
				self.to_forget.append(self.increase_amount_button)
				counter += 300

			if "Cars" in self.usable_layer and "Trees" in self.usable_layer and self.cars_enabled:
				self.swap_items_button = CButton(
					WidgetGeometry(270, 50, counter, 80),
					"Swap Cars with Trees",
					lambda _: self.swap_cars_with_trees(),
					self.content,
				)
				self.to_forget.append(self.swap_items_button)
				counter += 300

			if "Buildings" in self.usable_layer and self.buildings_enabled:
				self.cover_buildings_button = CButton(
					WidgetGeometry(270, 50, counter, 80),
					"Cover Buildings",
					lambda _: self.paint_buildings_green(),
					self.content,
				)
				self.to_forget.append(self.cover_buildings_button)
				counter += 300

		else:
			self.top_label["text"] = "No more trees can be added to this area"

		self.nick_name_label = Label(
			self.content, text="Scenario name: (Optional)", **self.layer_label_style
		)
		self.name_entry = Entry(self.content, **self.scale_style)

	def paint_buildings_green(self):
		"""
		Asks the user how much of the buildings should be covered by plants.
		:return: None
		"""
		for widget in self.to_forget:
			widget.place_forget()
		self.to_forget = []

		self.secondary_label["text"] = "How much of the buildings should be covered by plants?"

		# pylint: disable=W0201
		grid_index = (self.step_counter + 1) * 40
		self.buildings_to_paint_green_scale = Scale(
			self.content, from_=0, to=100, orient="horizontal", **self.scale_style
		)
		self.buildings_to_paint_green_scale.place(width=870, height=100, x=10, y=grid_index)
		self.to_forget.append(self.buildings_to_paint_green_scale)
		grid_index += 110

		confirm_button = CButton(
			WidgetGeometry(100, 50, 350, grid_index),
			"Confirm",
			lambda _: self.cleanup_paint_buildings(),
			self.content
		)

		self.to_forget.append(confirm_button)

	def cleanup_paint_buildings(self):
		"""
		Adds a step corresponding to covering some buildings by plants
		:return:
		"""
		increase_percentage = self.buildings_to_paint_green_scale.get() * 0.01
		buildings_to_cover = math.ceil((self.buildings_gdf.shape[0]) * increase_percentage)

		self.max_amount_buildings_coverable -= buildings_to_cover

		if self.max_amount_buildings_coverable <= 0:
			buildings_to_cover = self.buildings_gdf.shape[0]
			self.buildings_enabled = False

		self.modification_list.append(
			(ScenarioModificationType.PAINT_BUILDINGS_GREEN, buildings_to_cover)
		)
		self.add_another_step(ScenarioModificationType.PAINT_BUILDINGS_GREEN, buildings_to_cover)

	def add_more_trees(self):
		"""
		Asks the user how many more trees they want in percentage
		:return: None
		"""
		for widget in self.to_forget:
			widget.place_forget()
		self.to_forget = []

		self.secondary_label["text"] = "How many trees do you want to add in percentage?"

		# pylint: disable=W0201
		grid_index = (self.step_counter + 1) * 40
		self.increase_trees = Scale(
			self.content, from_=0, to=100, orient="horizontal", **self.scale_style
		)
		self.increase_trees.place(width=870, height=100, x=10, y=grid_index)
		self.to_forget.append(self.increase_trees)
		grid_index += 110

		confirm_button = CButton(
			WidgetGeometry(100, 50, 350, grid_index),
			"Confirm",
			lambda _: self.cleanup_more_trees(),
			self.content
		)

		self.to_forget.append(confirm_button)

	def swap_cars_with_trees(self):
		"""
		Prompts the user to enter how many of the cars should be swapped by trees.
		:return: None
		"""
		for widget in self.to_forget:
			widget.place_forget()
		self.to_forget = []

		self.secondary_label["text"] = "How many cars do you want to swap with trees in percentage?"

		# pylint: disable=W0201
		grid_index = (self.step_counter + 1) * 40
		self.trees_for_cars = Scale(
			self.content, from_=0, to=100, orient="horizontal", **self.scale_style
		)
		self.trees_for_cars.place(width=870, height=100, x=10, y=grid_index)
		self.to_forget.append(self.trees_for_cars)
		grid_index += 110

		confirm_button = CButton(
			WidgetGeometry(100, 50, 350, grid_index),
			"Confirm",
			lambda _: self.cleanup_swap_cars(),
			self.content
		)

		self.to_forget.append(confirm_button)

	def cleanup_more_trees(self):
		"""
		creates a gif with additional trees on it and displays that on the mainscreen
		:return: nothing (a gif is created, stored, logged and shown on the mainscreen)
		"""
		increase_percentage = self.increase_trees.get() * 0.01
		trees_to_add = math.ceil((self.tree_layer_panda.shape[0] - 1) * increase_percentage)

		self.modification_list.append((ScenarioModificationType.MORE_TREES, trees_to_add))
		self.add_another_step(ScenarioModificationType.MORE_TREES, trees_to_add)

	def cleanup_swap_cars(self):
		"""
		creates a gif with additional trees on it and displays that on the mainscreen
		:return: nothing (a gif is created, stored, logged and shown on the mainscreen)
		"""
		swap_percentag = self.trees_for_cars.get() * 0.01
		cars_to_swap = math.ceil((self.car_layer_panda.shape[0] - 1) * swap_percentag)

		self.max_amount_cars_swapable -= cars_to_swap

		if self.max_amount_cars_swapable <= 0:
			cars_to_swap = self.car_layer_panda.shape[0] - 1
			self.cars_enabled = False

		self.modification_list.append((ScenarioModificationType.SWAP_CARS, cars_to_swap))
		self.add_another_step(ScenarioModificationType.SWAP_CARS, cars_to_swap)

	def add_another_step(self, scenario_type, scenario_info):
		"""
		Adds another scenario step to the scenario that is being made.
		:param scenario_type: The type of step
		:param scenario_info: The information corresponding to the step
		:return: None
		"""
		for widget in self.to_forget:
			widget.place_forget()
		self.to_forget = []

		scenario_text = ""
		if scenario_type is ScenarioModificationType.MORE_TREES:
			scenario_text = "Add " + str(scenario_info) + " trees"
		if scenario_type is ScenarioModificationType.SWAP_CARS:
			scenario_text = "Swap " + str(scenario_info) + " cars with trees"
		if scenario_type is ScenarioModificationType.PAINT_BUILDINGS_GREEN:
			scenario_text = "Paint " + str(scenario_info) + " buildings green"

		grid_index = self.step_counter * 40

		step_info_label = Label(self.content, text=scenario_text, **self.layer_label_style)
		step_info_label.place(width=800, height=40, x=110, y=grid_index)

		grid_index += 40

		if self.step_counter < 5:
			self.step_counter += 1
			new_step_label = Label(
				self.top, text="Step " + str(self.step_counter), **self.layer_label_style
			)
			new_step_label.place(width=80, height=40, x=10, y=grid_index)

			self.secondary_label["text"
								] = "How do you want to increase the number of plants in this area?"
			self.secondary_label.place(width=800, height=40, x=110, y=grid_index)

			grid_index += 40
			counter = 10
			if "Trees" in self.usable_layer:
				self.increase_amount_button = CButton(
					WidgetGeometry(270, 50, counter, grid_index),
					"Add more Trees",
					lambda _: self.add_more_trees(),
					self.content,
				)
				self.to_forget.append(self.increase_amount_button)
				counter += 300

			if "Cars" in self.usable_layer and "Trees" in self.usable_layer and self.cars_enabled:
				self.swap_items_button = CButton(
					WidgetGeometry(270, 50, counter, grid_index),
					"Swap Cars with Trees",
					lambda _: self.swap_cars_with_trees(),
					self.content,
				)
				self.to_forget.append(self.swap_items_button)
				counter += 300

			if "Buildings" in self.usable_layer and self.buildings_enabled:
				self.cover_buildings_button = CButton(
					WidgetGeometry(270, 50, counter, grid_index),
					"Cover Buildings",
					lambda _: self.paint_buildings_green(),
					self.content,
				)
				self.to_forget.append(self.cover_buildings_button)
				counter += 300

		else:
			self.secondary_label.place_forget()

		grid_index += 60
		self.nick_name_label.place(width=350, height=40, x=10, y=grid_index)
		self.to_forget.append(self.nick_name_label)

		self.name_entry.place(width=530, height=40, x=350, y=grid_index)
		self.to_forget.append(self.name_entry)

		grid_index += 60
		confirm_button = CButton(
			WidgetGeometry(100, 50, 350, grid_index),
			"Confirm",
			lambda _: self.cleanup(),
			self.content
		)
		self.to_forget.append(confirm_button)

	def cleanup(self):
		"""
		Cleans up the GUI element and lets the application create a scenario for the request.
		:return:
		"""
		name = self.name_entry.get()
		if name == "":
			name = None

		self.top.destroy()

		self.application.create_scenario(
			request=self.application.current_request, modification_list=self.modification_list
		)
		self.main_screen.render_dynamic_widgets()
