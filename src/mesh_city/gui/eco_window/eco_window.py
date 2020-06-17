"""
The module containing the eco window
"""
import math
from tkinter import Button, Entry, Label, Scale, Toplevel

import pandas as pd

from mesh_city.request.layers.buildings_layer import BuildingsLayer
from mesh_city.request.layers.cars_layer import CarsLayer
from mesh_city.request.layers.google_layer import GoogleLayer
from mesh_city.request.layers.trees_layer import TreesLayer
from mesh_city.scenario.scenario_pipeline import ScenarioModificationType


class EcoWindow:
	"""
	Window showing all the options what the user can do to make the area downloaded more eco-friendly
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

		detected_layers = []
		for layer in self.application.current_request.layers:
			if isinstance(layer, GoogleLayer):
				detected_layers.append("Google Maps")
			if isinstance(layer, TreesLayer):
				detected_layers.append("Trees")
			if isinstance(layer, CarsLayer):
				detected_layers.append("Cars")
			if isinstance(layer, BuildingsLayer):
				detected_layers.append("Buildings")

		self.top_label = Label(self.top, text="")
		self.top_label.grid(row=0)

		usable_layers = []

		if "Trees" in detected_layers:
			self.tree_layer_panda = pd.read_csv(
				self.application.current_request.get_layer_of_type(TreesLayer).detections_path
			)
			if self.tree_layer_panda.shape[0] > 1:
				usable_layers.append("Trees")
		if "Cars" in detected_layers:
			self.car_layer_panda = pd.read_csv(
				self.application.current_request.get_layer_of_type(CarsLayer).detections_path
			)
			if self.car_layer_panda.shape[0] > 1:
				usable_layers.append("Cars")
				self.max_amount_cars_swapable = self.car_layer_panda.shape[0] - 1
		if "Buildings" in detected_layers:
			usable_layers.append("Buildings")

		if "Trees" in usable_layers or "Buidlings" in usable_layers:
			self.top_label["text"] = "Scenario Creator"
			self.top_label.grid(row=0, column=0, columnspan=3)

			self.step_counter = 1
			self.to_forget = []
			self.important_widgets = []
			self.scenario_list = []

			self.step_one_text_label = Label(self.top, text="Step 1")
			self.step_one_text_label.grid(row=1, column=0)

			secondary_label_text = "How do you want to make this area more ecofriendly?"
			self.secondary_label = Label(self.top, text=secondary_label_text)
			self.secondary_label.grid(row=1, column=1, columnspan=2)

			counter = 0

			if "Trees" in usable_layers:
				self.increase_amount_button = Button(
					self.top, text="Add more Trees", command=self.add_more_trees, bg="white"
				)
				self.increase_amount_button.grid(row=2, column=counter)
				self.to_forget.append(self.increase_amount_button)
				self.important_widgets.append(self.increase_amount_button)
				counter += 1

			if "Cars" and "Trees" in detected_layers:
				self.swap_items_button = Button(
					self.top,
					text="Swap Cars with Trees",
					command=self.swap_cars_with_trees,
					bg="white"
				)
				self.swap_items_button.grid(row=2, column=counter)
				self.to_forget.append(self.swap_items_button)
				self.important_widgets.append(self.swap_items_button)
				counter += 1

			if "Buildings" in usable_layers:
				self.cover_buildings_button = Button(
					self.top, text="Cover Buildings", command=None, bg="white"
				)
				self.cover_buildings_button.grid(row=2, column=counter)
				self.to_forget.append(self.cover_buildings_button)
				self.important_widgets.append(self.cover_buildings_button)
				counter += 1

			self.nick_name_label = Label(self.top, text="Scenario name: \n(Optional)")
			self.name_entry = Entry(self.top)
			self.confirm_button = Button(
				self.top, text="Create Scenario", command=self.cleanup, bg="white"
			)

		else:
			self.top_label["text"] = "This area can not be made more eco-friendly"
			self.top_label.grid(row=0)

	def add_more_trees(self):
		"""
		Asks the user how many more trees they want in percentage
		:return: None
		"""
		for widget in self.to_forget:
			widget.grid_forget()
		self.to_forget = []

		self.secondary_label["text"] = "How many trees do you want to add in percentage?"

		# pylint: disable=W0201
		grid_index = self.step_counter + 1
		self.increase_trees = Scale(self.top, from_=0, to=100, orient="horizontal")
		self.increase_trees.grid(row=grid_index, columnspan=3)
		self.to_forget.append(self.increase_trees)
		grid_index += 1

		confirm_button = Button(
			self.top, text="Confirm", command=self.cleanup_more_trees, bg="white"
		)
		confirm_button.grid(row=grid_index, columnspan=3)
		self.to_forget.append(confirm_button)

	def swap_cars_with_trees(self):
		"""
		Prompts the user to enter how much of the cars should be swapped by trees.
		:return: None
		"""
		for widget in self.to_forget:
			widget.grid_forget()
		self.to_forget = []

		self.secondary_label["text"] = "How many cars do you want to swap with trees in percentage?"

		# pylint: disable=W0201
		grid_index = self.step_counter + 1
		self.trees_for_cars = Scale(self.top, from_=0, to=100, orient="horizontal")
		self.trees_for_cars.grid(row=grid_index, columnspan=3)
		self.to_forget.append(self.trees_for_cars)
		grid_index += 1

		confirm_button = Button(
			self.top, text="Confirm", command=self.cleanup_swap_cars, bg="white"
		)
		confirm_button.grid(row=grid_index, columnspan=3)
		self.to_forget.append(confirm_button)

	def cleanup_more_trees(self):
		"""
		creates a gif with additional trees on it and displays that on the mainscreen
		:return: nothing (a gif is created, stored, logged and shown on the mainscreen)
		"""
		increase_percentage = self.increase_trees.get() * 0.01
		trees_to_add = math.ceil((self.tree_layer_panda.shape[0] - 1) * increase_percentage)

		self.scenario_list.append((ScenarioModificationType.MORE_TREES, trees_to_add))
		self.add_another_step(ScenarioModificationType.MORE_TREES, trees_to_add)

	def cleanup_swap_cars(self):
		"""
		creates a gif with additional trees on it and displays that on the mainscreen
		:return: nothing (a gif is created, stored, logged and shown on the mainscreen)
		"""
		swap_percentag = self.trees_for_cars.get() * 0.01 + 1
		cars_to_swap = math.ceil((self.car_layer_panda.shape[0] - 1) * swap_percentag)

		self.max_amount_cars_swapable -= cars_to_swap

		if self.max_amount_cars_swapable < 0:
			cars_to_swap = self.car_layer_panda.shape[0] - 1
			self.important_widgets.remove(self.swap_items_button)

		self.scenario_list.append((ScenarioModificationType.SWAP_CARS, cars_to_swap))
		self.add_another_step(ScenarioModificationType.SWAP_CARS, cars_to_swap)

	def add_another_step(self, scenario_type, scenario_info):
		"""
		Adds another scenario step to the scenario that is being made.
		:param scenario_type: The type of step
		:param scenario_info: The information corresponding to the step
		:return: None
		"""
		for widget in self.to_forget:
			widget.grid_forget()
		self.to_forget = []

		scenario_text = ""
		if scenario_type is ScenarioModificationType.MORE_TREES:
			scenario_text = "Add " + str(scenario_info) + " trees"
		if scenario_type is ScenarioModificationType.SWAP_CARS:
			scenario_text = "Swap " + str(scenario_info) + " cars with trees"

		step_info_label = Label(self.top, text=scenario_text)
		step_info_label.grid(row=self.step_counter, column=1)

		grid_index = self.step_counter + 1

		if self.step_counter < 5:
			self.step_counter += 1
			new_step_label = Label(self.top, text="Step " + str(self.step_counter))
			new_step_label.grid(row=grid_index, column=0)

			self.secondary_label["text"] = "How do you want to make this area more ecofriendly?"
			self.secondary_label.grid(row=grid_index, column=1, columnspan=2)

			grid_index += 1
			for counter, widget in enumerate(self.important_widgets):
				widget.grid(row=grid_index, column=counter)
				self.to_forget.append(widget)
		else:
			self.secondary_label.grid_forget()

		grid_index += 1
		self.nick_name_label.grid(row=grid_index, column=0)
		self.to_forget.append(self.nick_name_label)

		self.name_entry.grid(row=grid_index, column=1)
		self.to_forget.append(self.name_entry)

		grid_index += 1
		self.confirm_button.grid(row=grid_index, column=1)
		self.to_forget.append(self.confirm_button)

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
			request=self.application.current_request,
			scenarios_to_create=self.scenario_list,
			name=name
		)
