"""
This module provides a GUI interface that can be used to select different layers to appear over the
main_screen image such as an indication where all the trees are
"""
from tkinter import Button, Checkbutton, IntVar, Label, Toplevel

from mesh_city.request.google_layer import GoogleLayer
from mesh_city.request.trees_layer import TreesLayer


class LayersWindow:
	"""
	A GUI class with a layer selection interface.
	"""

	def __init__(self, master, application, main_screen):
		"""
		Constructs the basic GUI elements and prompts the user to tick all the layers to appear.
		Un-ticked layers are not shown
		:param master: the master tkinter object
		:param application: the global application context
		:param main_screen: the main screen of the application
		"""

		self.main_screen = main_screen
		self.master = master
		self.application = application
		top = self.top = Toplevel(master)

		detected_layers = []
		for layer in self.application.current_request.layers:
			if isinstance(layer, GoogleLayer):
				detected_layers.append("Google Maps")
			if isinstance(layer, TreesLayer):
				detected_layers.append("Trees")

		if len(detected_layers) == 0:
			self.top_label = Label(top, text="There are no layers to show. Detect something first.")
			self.top_label.grid(row=0)
		else:
			self.top_label = Label(top, text="Tick the layers you want to see")
			self.top_label.grid(row=0)

			counter = 1
			self.check_box_list = []
			self.temp_int_var_list = []

			for layer in detected_layers:
				if layer in self.main_screen.active_layers:
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
		for (index, element) in enumerate(self.temp_int_var_list):
			layer_mask.append(False)
			if element.get() == 1:
				layer_mask[index] = True
		self.application.load_request_specific_layers(
			request=self.application.current_request, layer_mask=layer_mask
		)
