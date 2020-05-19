"""
See :class:`.StartScreen`
"""

from datetime import datetime
from tkinter import Toplevel

from mesh_city.gui.name_popup_window import NamePopupWindow
from mesh_city.gui.register_popup_window import RegisterPopupWindow
from mesh_city.user.user_info import UserInfo


class StartScreen:
	""""
    This class is a start screen GUI element that opens one of two popups and passes the entered
    information to the application object. It also handles the greeting of the user with a popup and
    providing the application with the relevant user information to make api calls etc.
    """

	def __init__(self, master, application):
		"""
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

		application.late_init()

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
