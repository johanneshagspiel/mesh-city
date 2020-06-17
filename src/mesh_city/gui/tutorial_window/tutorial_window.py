"""
Module containing the tutorialwindow class
"""
from tkinter import Button, Label, Toplevel

from mesh_city.gui.search_window.search_window_start import SearchWindowStart


class TutorialWindow:
	"""
	In case the user has not yet made a request, the tutorial window is loaded. Currently, it shows points the
	user to the window where they can make their first request
	"""

	def __init__(self, master, application, main_screen):
		"""
		The user is presented with all the options of the tutorial. Currently, it shows points the
		user to the window where they can make their first request
		:param master: the master tkinter object
		:param application: the global application context
		:param main_screen: the main screen
		"""
		self.main_screen = main_screen
		self.master = master
		self.value = ""
		self.application = application
		self.image_path = self.application.file_handler.folder_overview['image_path']
		self.top = Toplevel(master)

		self.top.config(padx=4)
		self.top.config(pady=4)

		self.top_label = Label(
			self.top, text="It seems like this is the first time you use this application."
		)
		self.top_label.grid(row=0)

		self.search_button = Button(
			self.top, text="Click here to make your first request", command=self.cleanup, bg="white"
		)
		self.search_button.grid(row=1)

	def cleanup(self):
		"""
		Currently opens the search window where they can make their first request
		:return: nothing (the search window is opened)
		"""
		temp_window = SearchWindowStart(self.master, self.application, self.main_screen)
		self.top.destroy()
		self.main_screen.master.wait_window(temp_window.top)
