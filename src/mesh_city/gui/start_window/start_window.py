"""
See :class:`.StartScreen`
"""

from tkinter import Button, Label, Toplevel
from mesh_city.gui.start_window.create_new_user_window import CreateNewUserWindow


class StartWindow:
	"""
	The start screen where the user can select an existing account or make a new one
	"""

	def __init__(self, master, application):
		"""
		The user either selects and existing account or creates a new one
		:param master: the master tkinter object
		:param application: the global application context
		"""

		self.master = master
		self.application = application
		top = self.top = Toplevel(master)

		self.geometry = "200x200"
		self.top_label = Label(top, text="With which account do you want to log in?")
		self.top_label.grid(row=0, column=1)

		self.dic_users = self.application.log_manager.read_log(
			path=self.application.file_handler.folder_overview["users.json"], type_document="users.json"
		)

		counter = 1
		for key in self.dic_users.keys():
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

	def load_user(self, user):
		"""
		Method called when the user wants to login with an existing user
		:param name_user: the user name
		:return: nothing (changes to main screen and initializes the missing user information
		in the global application context)
		"""
		self.application.late_init(user)

		temp_path = self.application.file_handler.folder_overview["coordinate_overview.json"]
		self.application.log_manager.read_log(temp_path, "coordinate_overview.json")

		self.top.destroy()

	# pylint: disable=W0201
	def create_new_user(self):
		"""
		Method called when the user wants to create a new user.
		:return: nothing (changes to create new user window)
		"""
		self.window = CreateNewUserWindow(self.master, self.application)
		self.top.destroy()
		self.master.wait_window(self.window.top)
