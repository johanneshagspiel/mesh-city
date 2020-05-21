"""
This module provides a GUI interface that can be used to select different layers such as
the satellite layer or heightmap layer
"""

import os
from pathlib import Path
from tkinter import Button, Label, Toplevel


class LayersWindow:
	"""
	A GUI class with a layer selection interface.
	"""

	def __init__(self, master, application, main_screen):
		"""
		Constructs the basic GUI elements and prompts the user to select a layer.
		:param master: The Tk root of the GUI.
		:param main_screen:
		"""

		self.main_screen = main_screen
		self.master = master
		self.application = application
		self.value = ""

		top = self.top = Toplevel(master)

		self.top_label = Label(top, text="Which layer do you want to load?")
		self.top_label.grid(row=0, column=1)

		counter = 1

		directory_list = os.listdir(self.application.file_handler.folder_overview["active_tile_path"][0])

		if not "layers" in directory_list:
			self.top_label["text"] = "There are no layers to load"
		if "layers" in directory_list:
			for directory in os.listdir(self.application.file_handler.folder_overview["active_layer_path"][0]):
				if directory != "":
					name_directory = str(directory)
					if name_directory != self.main_screen.layer_active:
						self.temp_name = Button(
							self.top,
							text=name_directory,
							width=20,
							height=3,
							command=lambda name_directory=name_directory: self.load_layer(name_directory),
							bg="grey"
						)
						self.temp_name.grid(row=counter, column=1)
						counter += 1
					if self.main_screen.layer_active != "normal":
						self.temp_name = Button(
							self.top, text="normal", width=20, height=3, command=self.load_standard, bg="grey"
						)
						self.temp_name.grid(row=counter, column=1)

	def load_layer(self, name_directory):
		"""
		Loads the layer from the provided layer directory and updates the image on the main_screen.
		:param name_directory: The layer's directory.
		"""
		###TODO: what if layers on top of each other
		self.application.file_handler.change("active_image_path",
		                                     Path.joinpath(self.application.file_handler.folder_overview["active_layer_path"][0],
		                                                   name_directory))

		self.main_screen.update_image()
		self.main_screen.layer_active = str(name_directory)
		self.top.destroy()

	def load_standard(self):
		"""
		Loads the standard layer and updates the image on the main_screen.
		"""
		self.application.file_handler.folder_overview["active_image_path"][0] = \
			self.application.file_handler.folder_overview["active_layer_path"][0].parents[0]

		self.main_screen.update_image()
		self.main_screen.layer_active = "normal"
		self.top.destroy()
