from tkinter import Toplevel, Button, Label

class StartUpWindow:

	def __init__(self, master, application, main_screen):
		self.master = master
		self.value = ""
		self.application = application
		self.top = Toplevel(master)
		self.image_path = self.application.file_handler.folder_overview['image_path']

		# self.top_label = Label(self.top, text="Which request do you want to load?")
		# self.top_label.grid(row=0, column=1)
		#
		# counter = 1
		# for temp in self.image_path.glob('*'):
		# 	if temp.is_file() is False:
		# 		name_directory = temp.name
		# 		self.temp_name = Button(
		# 			self.top,
		# 			text=name_directory,
		# 			width=20,
		# 			height=3,
		# 			command=lambda name_directory=name_directory: self.load_request(name_directory),
		# 			bg="grey"
		# 		)
		# 		self.temp_name.grid(row=counter, column=1)
		# 		counter += 1
