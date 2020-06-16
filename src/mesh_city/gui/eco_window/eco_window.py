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
			if "Trees" in detected_layers:

				self.tree_layer_panda = pd.read_csv(self.application.current_request.get_layer_of_type(TreesLayer).detections_path)

				if self.tree_layer_panda.shape[0] == 1:

				 	self.top_label["text"] = "This area can not be made more eco-friendly"

				else:
					self.top_label["text"] = "How do you want to make this area more eco-friendly?"
					self.top_label.grid(row=0)

					self.more_trees = Button(
						self.top, text="Add more trees", command=self.add_more_trees, bg="white"
					)
					self.more_trees.grid(row=1)

	def add_more_trees(self):
		"""
		Asks the user how many more trees they want in percentage
		:return: nothing (creates a gif with additional trees on it and displays that on the mainscreen)
		"""
		self.more_trees.grid_forget()

		self.top_label["text"] = "How many trees do you want to add in percentage?"
		# pylint: disable=W0201
		self.tree_increase = Scale(self.top, from_=0, to=100, orient="horizontal")
		self.tree_increase.grid(row=1)

		nick_name_label = Label(self.top, text="Scenario name: \n(Optionl)")
		nick_name_label.grid(row=2,column=0)

		self.name_entry = Entry(self.top)
		self.name_entry.grid(row=2, column=1)

		confirm_button = Button(
			self.top, text="Confirm", command=self.cleanup_more_trees, bg="white"
		)
		confirm_button.grid(row=3)

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

		name = self.name_entry.get()
		if name == "":
			name = None

		self.application.create_scenario(
			request=self.application.current_request,
			scenario_to_create=[(ScenarioType.MORE_Trees, trees_to_add)],
			name=name
		)

		self.top.destroy()
