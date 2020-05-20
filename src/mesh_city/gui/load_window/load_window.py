"""
A module that contains the loading old request window
"""

import os
from pathlib import Path
from tkinter import Button, Label, Toplevel


class LoadWindow:
	"""
	A window to select an old request to load onto the map
	"""

	def __init__(self, master, application, mainscreen):
		"""
		The initialization method. Creates a button for each old request
		:param master: the root tkinter instance
		:param application: the global application context
		:param mainscreen: the screen from which loadwindow is called
		"""

		self.mainscreen = mainscreen
		self.master = master
		self.value = ""
		self.application = application
		self.image_path = self.application.file_handler.folder_overview['image_path'][0]
		top = self.top = Toplevel(master)

		self.top_label = Label(top, text="Which request do you want to load?")
		self.top_label.grid(row=0, column=1)

		counter = 1
		for directory in os.listdir(self.image_path):
			if directory != "":
				name_directory = str(directory)
				self.temp_name = Button(
					self.top,
					text=name_directory,
					width=20,
					height=3,
					command=lambda name_directory=name_directory: self.load_request(name_directory),
					bg="grey"
				)
				self.temp_name.grid(row=counter, column=1)
				counter += 1

	def load_request(self, name_directory):
		"""
		Loads an old request as the current request into the mainscreen
		:param name_directory: the directory where the request to be loaded is stored
		:return: nothing
		"""

		self.application.file_handler.folder_overview["active_tile_path"][0] = \
			Path.joinpath(self.application.file_handler.folder_overview["image_path"][0], name_directory, "0_tile_0_0")

		self.application.file_handler.folder_overview["active_image_path"][0] = \
			Path.joinpath(self.application.file_handler.folder_overview["image_path"][0], name_directory, "0_tile_0_0")

		self.application.file_handler.folder_overview["active_request_path"][0] = \
			self.application.file_handler.folder_overview["active_tile_path"][0].parents[0]

		self.mainscreen.update_image()
		self.mainscreen.layer_active = "normal"
		self.top.destroy()
