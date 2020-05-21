from tkinter import Button, Label, Toplevel, Checkbutton, IntVar
from mesh_city.detection.pipeline import Pipeline

class DetectionScreen:

	def __init__(self, master, application, main_screen):
		self.main_screen = main_screen
		self.master = master
		self.value = ""
		self.application = application
		self.top = Toplevel(master)

		self.top_label = Label(self.top,text="What do you want to detect?")
		self.top_label.grid(row=0)

		self.tree_button_variable = IntVar()
		self.tree_button = Checkbutton(self.top, text="Trees", variable= self.tree_button_variable)
		self.tree_button.grid(row=1)

		self.confirm_button = Button(self.top, text="Confirm", command = self.cleanup)
		self.confirm_button.grid(row=2)

	def cleanup(self):

		if self.tree_button_variable.get() == 1:
			Pipeline(application=self.application,type="trees", main_screen=self.main_screen)

		self.top.destroy()
