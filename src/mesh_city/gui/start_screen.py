from datetime import datetime
from tkinter import Button, Entry, Label, Toplevel

from mesh_city.user.user_info import UserInfo


class StartScreen:

	def __init__(self, master, application):
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
		application.user_info = application.user_info_handler.load_user_info()
		self.w = NamePopupWindow(self.master)
		self.master.wait_window(self.w.top)
		self.value = self.w.value

	def register_user(self, application):
		self.w = RegisterPopupWindow(self.master)
		self.master.wait_window(self.w.top)
		current_time = datetime.now()
		name, key, quota = self.w.value
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


class RegisterPopupWindow(object):

	def __init__(self, master):
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
		self.b = Button(top, text="OK", command=self.cleanup)
		self.b.grid(row=4, columnspan=3)

	def cleanup(self):
		self.value = (self.name_entry.get(), self.key_entry.get(), self.quotum_entry.get())
		self.top.destroy()


class NamePopupWindow(object):

	def __init__(self, master):
		self.value = ""
		top = self.top = Toplevel(master)
		Label(top, text="Please enter your name:").grid(row=0, columnspan=3)
		Label(top, text="Name").grid(row=1)
		self.name_entry = Entry(top)
		self.name_entry.grid(row=1, column=1)
		self.b = Button(top, text='Ok', command=self.cleanup)
		self.b.grid(row=4, columnspan=3)

	def cleanup(self):
		self.value = self.name_entry.get()
		self.top.destroy()
