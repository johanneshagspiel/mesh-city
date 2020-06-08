"""
A module containing the export window class
"""

import os
from pathlib import Path
from tkinter import Button, Checkbutton, filedialog, IntVar, Label, Toplevel


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
		active_request_id = self.application.current_request.request_id
		temp_text = "Active Request: Request " + str(active_request_id)
		self.current_request_button = Button(
			self.top,
			text=temp_text,
			width=20,
			height=3,
			command=lambda: self.load_request(self.application.current_request),
			bg="grey"
		)
		self.current_request_button.grid(row=1, column=0)
		for (index, request) in enumerate(self.application.request_manager.requests):
			if request.request_id != active_request_id:
				self.request_button = Button(
					self.top,
					text="Request "+str(request.request_id),
					width=20,
					height=3,
					command=lambda: self.
						load_request(request),
					bg="grey"
				)
				self.request_button.grid(row=index+2, column=0)


	def load_request(self, request):
		"""
		Loads the request. Then asks the user which features of this request to export
		:param name_directory: the directory where the request is stored
		:return: nothing (the window is updated to now show which features to export)
		"""
		self.application.set_current_request(request=request)

		self.top_label.configure(text="What do you want to export?")

		for layer in self.application.current_request.layers:

			for key in self.temp_building_instructions_request.instructions.keys():
				for sub_layer in self.temp_building_instructions_request.instructions[key]:
					if sub_layer != "Coordinates":
						if sub_layer == "Paths":
							temp_name = key + " Images"
						else:
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

				if temp_split[0] == "Google":
					if temp_split[2] == "Images":
						temp_to_move = ("Google Maps", "Paths")
					if temp_split[2] == "World":
						temp_to_move = ("Google Maps", "World Files")
				else:
					temp_to_move = (temp_split[0], temp_split[1])

				temp_request_creator.follow_move_instructions(
					temp_to_move, temp_building_instructions, temp_path
				)

			self.application.file_handler.change("active_request_path", self.old_path)
			self.top.destroy()
