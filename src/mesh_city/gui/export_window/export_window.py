from tkinter import Button, Checkbutton, IntVar, Label, Toplevel

class ExportWindow:

	def __init__(self, master, application, main_screen):
		self.main_screen = main_screen
		self.master = master
		self.value = ""
		self.application = application
		self.top = Toplevel(master)

		self.top_label = Label(self.top, text="What do you want to export?")
		self.top_label.grid(row=0)


