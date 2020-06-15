from tkinter import Button, Checkbutton, IntVar, Label, Toplevel

class DownloadProgressWindow:

	def __init__(self, master, application):
		"""
		The initialization method
		:param master: the master tkinter object
		:param application: the global application context
		:param main_screen: the main_screen of the application
		"""
		self.master = master
		self.application = application
		self.top = Toplevel(master)
