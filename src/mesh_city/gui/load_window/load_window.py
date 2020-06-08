"""
A module that contains the loading old request window
"""
import pickle
from pathlib import Path
from tkinter import Button, Label, Toplevel


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

		for (index, request) in enumerate(self.application.request_manager.requests):
			self.temp_name = Button(
				self.top,
				text="Request " + str(request.request_id),
				width=20,
				height=3,
				command=lambda button_request=request: self.load_request(button_request),
				bg="grey"
			)
			self.temp_name.grid(row=index + 1, column=1)

	def load_request(self, request):
		"""
		Loads an old request as the current request into the main_screen
		:param name_directory: the directory where the request to be loaded is stored
		:return: nothing
		"""
		self.application.set_current_request(request=request)
		self.main_screen.delete_text()

		self.top.destroy()
