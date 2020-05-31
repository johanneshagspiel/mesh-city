"""
Module containing the generate screen class
"""
from tkinter import Button, Label, Toplevel


class GenerateWindow:
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

		top = self.top = Toplevel(master)

		self.top_label = Label(top, text="What do you want to generate?")
		self.top_label.grid(row=0)

		self.map_button = Button(self.top, text="Map", command=self.create_map)
		self.map_button.grid(row=1)

	def create_map(self):
		"""
		Creates a map object and displays it on the main screen
		:return: nothing (displays a map on the main screen)
		"""
		self.main_screen.overlay_creator.create_map_image(["trees"])
		self.main_screen.update_image()
		self.top.destroy()
