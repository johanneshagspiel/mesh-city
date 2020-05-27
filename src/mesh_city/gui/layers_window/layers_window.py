"""
This module provides a GUI interface that can be used to select different layers to appear over the
main_screen image such as an indication where all the trees are
"""

from tkinter import Button, Checkbutton, IntVar, Label, Toplevel


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

		self.top_label = Label(top, text="Tick the layers you want to see")
		self.top_label.grid(row=0)

		counter = 1
		self.check_box_list = []
		self.temp_int_var_list = []

		if len(self.main_screen.overlay_creator.overlay_overview.items()) == 0:
			self.top_label.configure(text="There are no layers to load. Detect something first.")

		else:
			for key in self.main_screen.overlay_creator.overlay_overview.keys():
				if key in self.main_screen.active_layers:
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

		if temp_sum == 0:
			self.main_screen.active_layers = []
			self.application.file_handler.change(
				"active_image_path",
				self.application.file_handler.folder_overview["active_tile_path"]
			)
			self.main_screen.update_image()
			self.top.destroy()
		else:
			self.main_screen.overlay_creator.create_composite_image(overlays)
			self.main_screen.update_image()
			self.top.destroy()
