"""
A module containing the detection screen
"""
from tkinter import Button, Label, Toplevel, Checkbutton, IntVar
from mesh_city.detection.pipeline import Pipeline

class DetectionScreen:
	"""
	The detection screen where one can select what to detect i.e. trees. The main_screen then will be
	updated automatically
	"""

	def __init__(self, master, application, main_screen):
		"""
		The initialization method
		:param master: the master tkinter object
		:param application: the global application context
		:param main_screen: the main_screen of the application
		"""
		self.main_screen = main_screen
		self.master = master
		self.value = ""
		self.application = application
		self.top = Toplevel(master)

		self.top_label = Label(self.top,text="What do you want to detect?")
		self.top_label.grid(row=0)

		self.tree_button_variable = IntVar()
		self.tree_button = Checkbutton(self.top, text="trees", variable= self.tree_button_variable)
		self.tree_button.grid(row=1)

		self.confirm_button = Button(self.top, text="Confirm", command = self.cleanup)
		self.confirm_button.grid(row=2)

	def cleanup(self):
		"""
		Method called on button press: runs the appropriate detection algorithm, updates the image
		on the main_screen and then closes itself
		:return:
		"""

		if self.tree_button_variable.get() == 1:
			Pipeline(application=self.application, type_of_detection="trees", main_screen=self.main_screen)

		self.main_screen.update_image()
		self.top.destroy()
