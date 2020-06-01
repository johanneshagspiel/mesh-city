"""
This module provides a GUI interface that can be used to select different layers to appear over the
main_screen image such as an indication where all the trees are
"""
from pathlib import Path
from tkinter import Button, Checkbutton, IntVar, Label, Toplevel

from mesh_city.imagery_provider.request_creator import RequestCreator


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

		temp_path = next(self.application.file_handler.folder_overview["active_request_path"].glob('building_instructions_request_*'))
		self.building_instructions = self.application.log_manager.read_log(temp_path, "building_instructions_request")

		temp_list_detected_layers = []
		for key in self.building_instructions.instructions.keys():
			if key != "Google Maps":
				temp_list_detected_layers.append(key)

		if len(temp_list_detected_layers) == 0:
			self.top_label = Label(top, text="There are no layers to show. Detect something first.")
			self.top_label.grid(row=0)

		else:
			self.top_label = Label(top, text="Tick the layers you want to see")
			self.top_label.grid(row=0)

			counter = 1
			self.check_box_list = []
			self.temp_int_var_list = []

			for layer in temp_list_detected_layers:
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

		temp_counter = 0
		overlays = []
		temp_sum = 0

		for element in self.temp_int_var_list:
			if element.get() == 1:
				overlays.append(self.check_box_list[temp_counter].cget("text"))
				temp_sum += 1
			temp_counter += 1

		temp_request_creator = RequestCreator(application=self.application)
		if temp_sum == 0:
			self.main_screen.active_layers = []

			temp_path = Path.joinpath(self.application.file_handler.folder_overview["temp_image_path"],
			                          "concat_image_normal.png")
			# TODO change when using other satillte image providers
			temp_request_creator.follow_create_instructions(["Google Maps", "Paths"],
			                                                self.building_instructions,
			                                                temp_path)
			self.application.file_handler.change("active_image_path",
			                         self.application.file_handler.folder_overview["temp_image_path"])

			self.main_screen.delete_text()
			self.main_screen.update_image()
			self.top.destroy()

		else:
			temp_request_creator.create_overlay_image(self.building_instructions, overlays, (600, 600))

			self.main_screen.active_layers.extend(overlays)
			self.main_screen.update_image()
			self.top.destroy()
