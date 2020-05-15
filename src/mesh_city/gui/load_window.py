import os
from pathlib import Path
from tkinter import Button, Entry, Label, Toplevel

class LoadWindow(object):

	def __init__(self, master, application, mainscreen):
		self.mainscreen = mainscreen
		self.master = master
		self.value = ""
		self.application = application
		self.image_path = self.application.request_manager.images_folder_path
		top = self.top = Toplevel(master)

		self.top_label = Label(top,text="Which request do you want to load?")
		self.top_label.grid(row=0, column=1)

		counter = 1
		for directory in os.listdir(self.image_path):
			if(directory != ""):
				name_directory = str(directory)
				temp_name = name_directory + "_" + str(counter) + "_button"
				self.temp_name = Button(self.top, text=name_directory, width=20, height=3, command=lambda name_directory=name_directory: self.load_request(name_directory), bg="grey")
				self.temp_name.grid(row = counter, column = 1)
				counter += 1

	def load_request(self, name_directory):
		self.mainscreen.currently_active_tile = Path.joinpath(self.image_path, name_directory, "0_tile_0_0")
		self.mainscreen.currently_active_request = Path(self.mainscreen.currently_active_tile).parents[0]
		self.mainscreen.update_Image()
		self.mainscreen.layer_active = False
		self.top.destroy()
