"""
The module containing the eco window
"""
import math
import pandas as pd

from tkinter import Button, Label, Scale, Toplevel, Entry

from mesh_city.request.layers.buildings_layer import BuildingsLayer
from mesh_city.request.layers.cars_layer import CarsLayer
from mesh_city.request.layers.google_layer import GoogleLayer
from mesh_city.request.layers.trees_layer import TreesLayer
from mesh_city.request.scenario.scenario_pipeline import ScenarioType


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

		if len(detected_layers) == 1:
			self.top_label["text"
			] = "This area can not be made more eco-friendly. Detect something first"

		else:
			usable_layers = []

			if "Trees" in detected_layers:
				self.tree_layer_panda = pd.read_csv(self.application.current_request.get_layer_of_type(TreesLayer).detections_path)
				if self.tree_layer_panda.shape[0] > 1:
					usable_layers.append("Trees")
			if "Cars" in detected_layers:
				self.car_layer_panda = pd.read_csv(
					self.application.current_request.get_layer_of_type(
						CarsLayer).detections_path)
				if self.car_layer_panda.shape[0] > 1:
					usable_layers.append("Cars")
			if "Buildings" in detected_layers:
				usable_layers.append("Buildings")

			if "Trees" or "Buidlings" in usable_layers:
				self.top_label["text"] = "Scenario Creator"
				self.top_label.grid(row=0,column=0, columnspan=3)

				self.step_counter = 1
				self.to_forget = []
				self.option_buttons = []

				step_text = "Step " + str(self.step_counter)
				self.step_text_label = Label(self.top, text=step_text)
				self.step_text_label.grid(row=1, column=0)

				secondary_label_text = "How do you want to make this area more ecofriendly?"
				self.secondary_label = Label(self.top, text=secondary_label_text)
				self.secondary_label.grid(row=1, column=1, columnspan=2)

				counter = 0

				if "Trees" in usable_layers:
					self.increase_amount_button = Button(
						self.top, text="Add more Trees", command=self.add_more_trees, bg="white"
					)
					self.increase_amount_button.grid(row=2,column=counter)
					self.to_forget.append(self.increase_amount_button)
					self.option_buttons.append(self.increase_amount_button)
					counter += 1

				if "Cars" and "Trees" in detected_layers:
					self.swap_items_button = Button(
						self.top, text="Swap Cars with Trees", command=None, bg="white"
					)
					self.swap_items_button.grid(row=2,column=counter)
					self.to_forget.append(self.swap_items_button)
					self.option_buttons.append(self.swap_items_button)
					counter+=1

				if "Buildings" in usable_layers:
					self.cover_buildings_button = Button(
						self.top, text="Cover Buildings", command=None, bg="white"
					)
					self.cover_buildings_button.grid(row=2,column=counter)
					self.to_forget.append(self.cover_buildings_button)
					self.option_buttons.append(self.cover_buildings_button)
					counter += 1

				self.nick_name_label = Label(self.top, text="Scenario name: \n(Optionl)")
				self.name_entry = Entry(self.top)

			else:
				self.top_label["text"] = "This area can not be made more eco-friendly"

	def add_more_trees(self):
		"""
		Asks the user how many more trees they want in percentage
		:return: nothing (creates a gif with additional trees on it and displays that on the mainscreen)
		"""
		for widget in self.to_forget:
			widget.grid_forget()
		self.to_forget= []

		self.secondary_label["text"] = "How many trees do you want to add in percentage?"

		# pylint: disable=W0201
		self.tree_increase = Scale(self.top, from_=0, to=100, orient="horizontal")
		self.tree_increase.grid(row=2, columnspan=3)
		self.to_forget.append(self.tree_increase)

		confirm_button = Button(
			self.top, text="Confirm", command=None, bg="white"
		)
		confirm_button.grid(row=3, columnspan=3)
		self.to_forget.append(confirm_button)

	def add_another_step(self):

		for widget in self.to_forget:
			widget.grid_forget()
		self.to_forget = []

		self.nick_name_label.grid(row=2, column=0)
		self.name_entry.grid(row=2, column=1)

	def cleanup_more_trees(self):
		"""
		creates a gif with additional trees on it and displays that on the mainscreen
		:return: nothing (a gif is created, stored, logged and shown on the mainscreen)
		"""
		increase_percentage = self.tree_increase.get() * 0.01 + 1
		trees_to_add = math.ceil(
			(self.tree_layer_panda.shape[0] - 1) * increase_percentage -
			(self.tree_layer_panda.shape[0] - 1)
		)

	def cleanup(self):
		name = self.name_entry.get()
		if name == "":
			name = None

		self.application.create_scenario(
			request=self.application.current_request,
			scenario_to_create=[(ScenarioType.MORE_Trees, trees_to_add)],
			name=name
		)

		self.top.destroy()
