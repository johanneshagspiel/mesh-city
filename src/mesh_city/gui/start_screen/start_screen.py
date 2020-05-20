"""
See :class:`.StartScreen`
"""

from tkinter import Toplevel, Label, Button
from mesh_city.gui.start_screen.create_new_user_window import CreateNewUserWindow



class StartScreen:

	def __init__(self, master, application):

		self.value = ""
		self.master = master
		self.application = application
		top = self.top = Toplevel(master)

		self.geometry = "200x200"
		self.top_label = Label(top, text="With which account do you want to log in?")
		self.top_label.grid(row=0, column=1)

		self.dic_users = self.application.log_manager.read_log(
			path=self.application.file_handler.folder_overview["users.json"])

		counter = 1
		for key, value in self.dic_users.items():
			name_user = key
			self.temp_name = Button(
				self.top,
				text=name_user,
				width=20,
				height=3,
				command=lambda name_user=name_user: self.load_user(self.dic_users[name_user]),
				bg="grey"
			)
			self.temp_name.grid(row=counter, column=1)
			counter += 1

		self.create_user = Button(
			self.top,
			text="Create a new user",
			width=20,
			height=3,
			command=self.create_new_user,
			bg="grey"
		)
		self.create_user.grid(row=counter, column=1)

	def load_user(self, name_user):
		self.application.late_init(name_user)
		self.top.destroy()

	def create_new_user(self):
		self.window = CreateNewUserWindow(self.master, self.application)
		self.top.destroy()
		self.master.wait_window(self.window.top)
