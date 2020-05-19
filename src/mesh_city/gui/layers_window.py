"""This module provides a GUI interface that can be used to select different layers such as
the satellite layer or heightmap layer"""
import os
from pathlib import Path
from tkinter import Button, Label, Toplevel


class LayersWindow:
	"""
	A GUI class with a layer selection interface.
	"""

	def __init__(self, master, main_screen):
		"""
		Constructs the basic GUI elements and prompts the user to select a layer.
		:param master: The Tk root of the GUI.
		:param main_screen:
		"""
		self.main_screen = main_screen
		self.master = master
		self.value = ""
		self.currently_active_tile = self.main_screen.currently_active_tile
		top = self.top = Toplevel(master)

		self.top_label = Label(top, text="Which layer do you want to load?")
		self.top_label.grid(row=0, column=1)

		counter = 1

		directory_list = os.listdir(self.currently_active_tile)

		if not "layers" in directory_list and not self.main_screen.layer_active:
			self.top_label["text"] = "There are no layers to load"
		if "layers" in directory_list:
			self.layers_folder = Path.joinpath(self.currently_active_tile, "layers")
			for directory in os.listdir(self.layers_folder):
				if directory != "":
					name_directory = str(directory)
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
		if self.main_screen.layer_active:
			self.temp_name = Button(
				self.top, text="Normal", width=20, height=3, command=self.load_standard, bg="grey"
			)
			self.temp_name.grid(row=counter, column=1)

	def load_layer(self, name_directory):
		"""
		Loads the layer from the provided layer directory and updates the image on the main_screen.
		:param name_directory: The layer's directory.
		"""
		self.main_screen.currently_active_tile = Path.joinpath(self.layers_folder, name_directory)
		self.main_screen.update_image()
		self.main_screen.layer_active = True
		self.top.destroy()

	def load_standard(self):
		"""
		Loads the standard layer and updates the image on the main_screen.
		"""
		self.main_screen.currently_active_tile = self.main_screen.currently_active_tile.parents[1]
		self.main_screen.update_image()
		self.main_screen.layer_active = False
		self.top.destroy()
