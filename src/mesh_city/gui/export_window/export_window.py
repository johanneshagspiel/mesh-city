"""
A module containing the export window class
"""

import os
from pathlib import Path
from tkinter import Button, Checkbutton, filedialog, IntVar, Label, Toplevel

from mesh_city.imagery_provider.request_creator import RequestCreator


class ExportWindow:
	"""
	The window where the user can select what they want to export as well as where to export that to
	"""

	def __init__(self, master, application):
		"""
		First asks the user which request to export
		:param master: the master tkinter application
		:param application: the global application context
		"""
		self.master = master
		self.value = ""
		self.application = application
		self.top = Toplevel(master)
		self.image_path = self.application.file_handler.folder_overview['image_path']

		self.top_label = Label(self.top, text="Which request do you want to export?")
		self.top_label.grid(row=0)

		self.temp_list = []
		name_active_request = self.application.file_handler.folder_overview["active_request_path"
																			].name
		temp_text = "Active Request: " + name_active_request
		self.temp_name = Button(
			self.top,
			text=temp_text,
			width=20,
			height=3,
			command=lambda name_active_request=name_active_request: self.
			load_request(name_active_request),
			bg="grey"
		)
		self.temp_name.grid(row=1, column=0)
		self.temp_list.append(self.temp_name)

		counter = 2
		for temp in self.image_path.glob('*'):
			if temp.is_file() is False:
				name_directory = temp.name
				if name_directory != name_active_request:
					self.temp_name = Button(
						self.top,
						text=name_directory,
						width=20,
						height=3,
						command=lambda name_directory=name_directory: self.
						load_request(name_directory),
						bg="grey"
					)
					self.temp_name.grid(row=counter, column=0)
					counter += 1
					self.temp_list.append(self.temp_name)

	def load_request(self, name_directory):
		"""
		Loads the request. Then asks the user which features of this request to export
		:param name_directory: the directory where the request is stored
		:return: nothing (the window is updated to now show which features to export)
		"""

		self.name_directory = name_directory

		self.old_path = self.application.file_handler.folder_overview["active_request_path"]

		self.application.file_handler.change(
			"active_request_path",
			Path.joinpath(self.application.file_handler.folder_overview["image_path"], name_directory)
		)

		temp_path = next(
			self.application.file_handler.folder_overview["active_request_path"].
			glob("building_instructions_*")
		)

		self.temp_building_instructions_request = self.application.log_manager.read_log(
			path=temp_path, type_document="building_instructions_request"
		)

		self.top_label.configure(text="What do you want to export?")

		for temp_button in self.temp_list:
			temp_button.grid_forget()

		temp_list_detected_layers = []
		for key in self.temp_building_instructions_request.instructions.keys():
			for sub_layer in self.temp_building_instructions_request.instructions[key]:
				temp_name = key + " " + sub_layer
				temp_list_detected_layers.append(temp_name)

		counter = 1
		self.check_box_list = []
		self.temp_int_var_list = []
		for layer in temp_list_detected_layers:
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
		Asks the user to select a folder to export to. Then copies all the files into this folder
		:return: nothing (the desired images are exported to a folder)
		"""

		to_export = []
		temp_counter = 0
		temp_sum = 0
		temp_request_creator = RequestCreator(self.application)
		temp_path = next(
			self.application.file_handler.folder_overview["active_request_path"].
			glob("building_instructions_request*")
		)
		temp_building_instructions = self.application.log_manager.read_log(
			temp_path, "building_instructions_request"
		)

		for element in self.temp_int_var_list:
			if element.get() == 1:
				to_export.append(self.check_box_list[temp_counter].cget("text"))
				temp_sum += 1
			temp_counter += 1

		if temp_sum == 0:
			self.application.file_handler.change("active_request_path", self.old_path)
			self.top.destroy()

		else:
			directory_to_store = Path(filedialog.askdirectory())
			temp_new_name = self.name_directory
			temp_new_path = Path.joinpath(directory_to_store, temp_new_name)
			# TODO: check whenever we make a directory that it does not already exist
			os.makedirs(temp_new_path)

			for element in to_export:
				temp_path = Path.joinpath(temp_new_path, element)
				os.makedirs(temp_path)

				temp_split = element.split(" ")
				temp_to_move = None

				if temp_split[0] == "Google" and temp_split[2] == "Paths":
					temp_to_move = ("Google Maps", "Paths")
				if temp_split[0] == "Google" and temp_split[2] == "World":
					temp_to_move = ("Google Maps", "World Files")
				if temp_split[0] == "Google" and temp_split[2] == "Coordinates":
					pass
				else:
					temp_to_move = (temp_split[0], temp_split[1])
				print(temp_to_move)

				temp_request_creator.follow_move_instructions(
					temp_to_move, temp_building_instructions, temp_path
				)

			self.application.file_handler.change("active_request_path", self.old_path)
			self.top.destroy()
