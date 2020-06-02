"""
Module containing the generate screen class
"""
from tkinter import Button, Label, Toplevel
from mesh_city.imagery_provider.request_creator import RequestCreator

class MapWindow:
	"""
	The generate screen class where the user can select things they want to generate like a map
	"""

	def __init__(self, master, application, main_screen):
		"""
		The user is asked to select what they want to generate
		:param master: the master tkinter object
		:param application: the global application context
		:param main_screen: the main screen of the application
		"""
		self.main_screen = main_screen
		self.master = master
		self.application = application
		self.main_screen = main_screen

		self.request_creator = RequestCreator(self.application)

		top = self.top = Toplevel(master)

		# TODO update with new detection options
		self.list_detection_options = ["Trees"]

		self.top_label = Label(top, text="Do you want to generate a map?")
		self.top_label.grid(row=0)

		temp_path = next(self.application.file_handler.folder_overview["active_request_path"].glob('building_instructions_request_*'))
		building_instructions = self.application.log_manager.read_log(temp_path, "building_instructions_request")

		self.temp_list_detected_layers = []
		for key in building_instructions.instructions.keys():
			# TODO change if we ever add another image provider
			if key != "Google Maps":
				self.temp_list_detected_layers.append(key)

		if len(self.temp_list_detected_layers) == 0:
			self.top_label["text"] = "A map can not be generated. Detect something first."

		else:
			self.map_button = Button(self.top, text="Map",
			                         command= lambda : self.create_map(building_instructions),
			                         bg="white")
			self.map_button.grid(row=1)

	def create_map(self, building_instructions):
		"""
		Creates a map object and displays it on the main screen
		:return: nothing (displays a map on the main screen)
		"""
		# self.main_screen.overlay_creator.create_map_image(["trees"])

		self.request_creator.create_map_image(building_instructions, self.temp_list_detected_layers)

		self.main_screen.update_image()
		self.top.destroy()
