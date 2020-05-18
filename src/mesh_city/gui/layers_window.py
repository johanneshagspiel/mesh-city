import os
from pathlib import Path
from tkinter import Button, Entry, Label, Toplevel


class LayersWindow(object):

	def __init__(self, master, application, mainscreen):
		self.mainscreen = mainscreen
		self.master = master
		self.value = ""
		self.application = application
		self.currently_active_tile = self.mainscreen.currently_active_tile
		top = self.top = Toplevel(master)

		self.top_label = Label(top, text="Which layer do you want to load?")
		self.top_label.grid(row=0, column=1)

		counter = 1

		directory_list = os.listdir(self.currently_active_tile)

		if (False == ("layers" in directory_list) and (False == self.mainscreen.layer_active)):
			self.top_label["text"] = "There are no layers to load"
		if ("layers" in directory_list):
			self.layers_folder = Path.joinpath(self.currently_active_tile, "layers")
			for directory in os.listdir(self.layers_folder):
				if (directory != ""):
					name_directory = str(directory)
					temp_name = name_directory + "_" + str(counter) + "_button"
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
		if (self.mainscreen.layer_active == True):
			self.temp_name = Button(
				self.top, text="Normal", width=20, height=3, command=self.load_standard, bg="grey"
			)
			self.temp_name.grid(row=counter, column=1)

	def load_layer(self, name_directory):
		self.mainscreen.currently_active_tile = Path.joinpath(self.layers_folder, name_directory)
		self.mainscreen.update_image()
		self.mainscreen.layer_active = True
		self.top.destroy()

	def load_standard(self):
		self.mainscreen.currently_active_tile = self.mainscreen.currently_active_tile.parents[1]
		self.mainscreen.update_image()
		self.mainscreen.layer_active = False
		self.top.destroy()
