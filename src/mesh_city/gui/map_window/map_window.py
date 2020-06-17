from tkinter import Button, Checkbutton, IntVar, Label, Toplevel

from mesh_city.request.layers.buildings_layer import BuildingsLayer
from mesh_city.request.layers.cars_layer import CarsLayer
from mesh_city.request.layers.google_layer import GoogleLayer
from mesh_city.request.layers.trees_layer import TreesLayer


class MapWindow:


	def __init__(self, master, application, main_screen):

		self.main_screen = main_screen
		self.master = master
		self.application = application
		top = self.top = Toplevel(master)

		detected_layers = []
		for layer in self.application.current_request.layers:
			if isinstance(layer, TreesLayer):
				detected_layers.append("Trees")
			if isinstance(layer, CarsLayer):
				detected_layers.append("Cars")
			if isinstance(layer, BuildingsLayer):
				detected_layers.append("Buildings")

		if len(detected_layers) == 0:
			self.top_label = Label(top, text="No map can be generated. Detect something first.")
			self.top_label.grid(row=0)
		else:
			self.top_label = Label(top, text="Tick the elements you want to see on the map")
			self.top_label.grid(row=0)

			counter = 1
			self.check_box_list = []
			self.temp_int_var_list = []

			for layer in detected_layers:
				if layer in self.main_screen.generated_content:
					self.temp_int_var_list.append(IntVar(value=1))
				else:
					self.temp_int_var_list.append(IntVar())
				self.check_box_list.append(
					Checkbutton(self.top, text=layer, variable=self.temp_int_var_list[counter - 1])
				)
				self.check_box_list[counter - 1].grid(row=counter)
				counter += 1

				self.confirm_button = Button(self.top, text="Confirm", command=self.cleanup)
				self.confirm_button.grid(row=counter)

	def cleanup(self):
		"""
		The method called when clicking on the confirm button. It checks which layers where chosen
		to appear and creates the appropriate overlay image which then appears on the main screen
		:return: nothing (but it updates the image on the main screen)
		"""
		layer_mask = []
		new_generated_content = []
		for (index, element) in enumerate(self.temp_int_var_list):
			if element.get() == 1:
				layer_mask.append(self.check_box_list[index].cget("text"))

		for (index, element) in enumerate(layer_mask):
			if element == "Trees":
				for layer in self.application.current_request.layers:
					if isinstance(layer, TreesLayer):
						layer_mask[index] = layer
						new_generated_content.append("Trees")
			if element == "Cars":
				for layer in self.application.current_request.layers:
					if isinstance(layer, CarsLayer):
						layer_mask[index] = layer
						new_generated_content.append("Cars")
			if element == "Buildings":
				for layer in self.application.current_request.layers:
					if isinstance(layer, BuildingsLayer):
						layer_mask[index] = layer
						new_generated_content.append("Buildings")

		self.main_screen.generated_content = new_generated_content
		self.application.create_map(
			request=self.application.current_request, layer_mask=layer_mask
		)
		self.top.destroy()
