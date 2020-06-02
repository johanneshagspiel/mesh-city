"""
A module that contains the loading old request window
"""

from pathlib import Path
from tkinter import Button, Label, Toplevel

from mesh_city.imagery_provider.request_creator import RequestCreator


class LoadWindow:
	"""
	A window to select an old request to load onto the map
	"""

	def __init__(self, master, application, main_screen):
		"""
		The initialization method. Creates a button for each old request
		:param master: the root tkinter instance
		:param application: the global application context
		:param mainscreen: the screen from which loadwindow is called
		"""

		self.main_screen = main_screen
		self.master = master
		self.value = ""
		self.application = application
		self.image_path = self.application.file_handler.folder_overview['image_path']
		top = self.top = Toplevel(master)

		self.top_label = Label(top, text="Which request do you want to load?")
		self.top_label.grid(row=0, column=1)

		counter = 1
		for temp in self.image_path.glob('*'):
			if temp.is_file() is False:
				name_directory = temp.name
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
		Loads an old request as the current request into the main_screen
		:param name_directory: the directory where the request to be loaded is stored
		:return: nothing
		"""

		self.application.file_handler.folder_overview["active_tile_path"] = Path.joinpath(
			self.application.file_handler.folder_overview["image_path"], name_directory, "0_tile_0_0"
		)

		self.application.file_handler.folder_overview["active_image_path"] = Path.joinpath(
			self.application.file_handler.folder_overview["image_path"], name_directory, "0_tile_0_0"
		)

		self.application.file_handler.folder_overview[
			"active_request_path"] = self.application.file_handler.folder_overview["active_tile_path"
																				].parents[0]

		temp_path = next(
			self.application.file_handler.folder_overview["active_request_path"].
			glob("building_instructions_*")
		)

		temp_building_instructions_request = self.application.log_manager.read_log(
			path=temp_path, type_document="building_instructions_request"
		)

		temp_request_creator = RequestCreator(application=self.application)
		temp_path = Path.joinpath(
			self.application.file_handler.folder_overview["temp_image_path"],
			"concat_image_normal.png"
		)
		# TODO change when using other satillte image providers
		temp_request_creator.follow_create_instructions(
			["Google Maps", "Paths"], temp_building_instructions_request, temp_path
		)
		self.application.file_handler.change(
			"active_image_path", self.application.file_handler.folder_overview["temp_image_path"]
		)

		self.main_screen.update_image()
		self.main_screen.layer_active = "Google Maps"
		self.main_screen.delete_text()

		self.top.destroy()
