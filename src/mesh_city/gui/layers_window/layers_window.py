"""
This module provides a GUI interface that can be used to select different layers such as
the satellite layer or heightmap layer
"""

import os
from pathlib import Path
from tkinter import Button, Checkbutton, IntVar, Label, Toplevel


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

		self.top_label = Label(top, text="Tick the layers you want to see")
		self.top_label.grid(row=0)

		counter = 1
		self.check_box_list = []
		self.temp_int_var_list = []

		if len(self.main_screen.overlay_creator.overlay_overview.items()) == 0:
			self.top_label.configure(text="There are no layers to load. Detect something first.")

		else:
			for key, value in self.main_screen.overlay_creator.overlay_overview.items():
				print(self.main_screen.active_layers)
				print(key)
				if key in self.main_screen.active_layers:
					print("hi")
					self.temp_int_var_list.append(IntVar(value=1))
				else:
					self.temp_int_var_list.append(IntVar())
				self.check_box_list.append(
					Checkbutton(self.top, text=key, variable=self.temp_int_var_list[counter - 1])
				)
				self.check_box_list[counter - 1].grid(row=counter)
				counter += 1

			self.confirm_button = Button(self.top, text="Confirm", command=self.cleanup)
			self.confirm_button.grid(row=counter)

	def cleanup(self):

		temp_counter = 0
		overlays = []
		sum = 0

		for element in self.temp_int_var_list:
			if element.get() == 1:
				overlays.append(self.check_box_list[temp_counter].cget("text"))
				sum += 1
			temp_counter += 1

		if sum == 0:
			self.main_screen.active_layers = []
			self.application.file_handler.change(
				"active_image_path",
				self.application.file_handler.folder_overview["active_tile_path"][0]
			)
			self.main_screen.update_image()
			self.top.destroy()
		else:
			self.main_screen.overlay_creator.create_composite_image(overlays)
			self.main_screen.update_image()
			self.top.destroy()
