"""This module handles the greeting of the user with a popup and providing the application with the
relevant user information to make api calls etc."""
from datetime import datetime
from tkinter import Button, Entry, Label, Toplevel

from mesh_city.user.user_info import UserInfo


class StartScreen:
	""""
    This class is a start screen GUI element that opens one of two popups and passes the entered information to the
    application object.
    """

	def __init__(self, master, application):
		"""
        Initializes
        :param master: The Tkinter root
        :param application: The application object that should be invoked after the user has filled in their data.
        """
		self.value = ""
		self.master = master

		top = self.top = Toplevel(master)
		top.withdraw()

		if application.user_info_handler.file_exists():
			self.ask_for_name(application)
		else:
			self.register_user(application)

		application.update_after_start()

	def ask_for_name(self, application):
		"""
		Asks for the username and via a popup and loads this into the application.
		:param application: The application the username is loaded into.
		:return: None
		..todo:: Use the returned username and check it against persisted user info.
		"""
		application.user_info = application.user_info_handler.load_user_info()
		self.window = NamePopupWindow(self.master)
		self.master.wait_window(self.window.top)
		self.value = self.window.value

	def register_user(self, application):
		"""
        Asks the user for the relevant information to register a user account and loads this into
        the application object.
        :param application: The application object the registered user data is loaded into.
        """
		self.window = RegisterPopupWindow(self.master)
		self.master.wait_window(self.window.top)
		current_time = datetime.now()
		name, key, quota = self.window.value
		application.user_info = UserInfo(
			name,
			key,
			quota,
			0,
			current_time.year,
			current_time.month,
			current_time.day,
			current_time.hour,
			current_time.minute,
			current_time.second,
		)


class RegisterPopupWindow:
	"""
    A popup window class with fields for entering a name, api key and monthly quota and stores this
    data as its value.
    """

	def __init__(self, master):
		"""
		Sets up the interface of the popup.
        :param master: The TK root
        """
		self.value = ""
		self.geometry = ("200x200")
		top = self.top = Toplevel(master)
		Label(top,
			text="Please enter the following information to start collecting maps data:").grid(
			row=0, columnspan=3
			)
		Label(top, text="Name").grid(row=1)
		Label(top, text="Google API key").grid(row=2)
		Label(top, text="Monthly quota").grid(row=3)
		self.name_entry = Entry(top)
		self.key_entry = Entry(top)
		self.quotum_entry = Entry(top)
		self.name_entry.grid(row=1, column=1)
		self.key_entry.grid(row=2, column=1)
		self.quotum_entry.grid(row=3, column=1)
		self.button = Button(top, text="OK", command=self.cleanup)
		self.button.grid(row=4, columnspan=3)

	def cleanup(self):
		""""
		Destroys the onscreen GUI element and stores the entered values.
		"""
		self.value = (self.name_entry.get(), self.key_entry.get(), self.quotum_entry.get())
		self.top.destroy()


class NamePopupWindow:
	"""
    A popup window class with fields for entering a name that is stored as its value.
    """

	def __init__(self, master):
		"""
		Sets up the interface of the popup.
		:param master: The TK root
		"""
		self.value = ""
		top = self.top = Toplevel(master)
		Label(top, text="Please enter your name:").grid(row=0, columnspan=3)
		Label(top, text="Name").grid(row=1)
		self.name_entry = Entry(top)
		self.name_entry.grid(row=1, column=1)
		self.button = Button(top, text='Ok', command=self.cleanup)
		self.button.grid(row=4, columnspan=3)

	def cleanup(self):
		""""
		Destroys the onscreen GUI element and stores the entered value.
		"""
		self.value = self.name_entry.get()
		self.top.destroy()
