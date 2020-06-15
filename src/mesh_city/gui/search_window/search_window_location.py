"""
See :class:`.SearchWindowLocation`
"""
from tkinter import Button, Entry, Label, Toplevel, messagebox

from mesh_city.gui.search_window.preview_window import PreviewWindow
from mesh_city.util.input_util import InputUtil


class SearchWindowLocation:
	"""
	A pop-up type GUI element that the user can fill in to make a location-type request.
	.. todo:: Make a pop-up class that this inherits from.
	"""

	def __init__(self, master, application, main_screen):
		"""
		Initializes the GUI elements of the pop-up and sets up callbacks
		:param master: The Tk root.
		:param application: The application object that is used to make requests.
		:param main_screen: The main screen object the popups interacts with.
		"""
		self.main_screen = main_screen
		self.master = master
		self.value = ""
		self.application = application
		top = self.top = Toplevel(master)

		self.top.config(padx=4)
		self.top.config(pady=4)

		Label(top, text="Which location are you interested in downloading ?").grid(row=0, column=3)

		self.latitude = Label(top, text="Latitude:")
		self.latitude.grid(row=1, column=1)
		self.longitude = Label(top, text="Longitude:")
		self.longitude.grid(row=2, column=1)

		self.lat_entry = Entry(top, width=20)
		self.lat_entry.grid(row=1, column=3)
		self.long_entry = Entry(top, width=20)
		self.long_entry.grid(row=2, column=3)

		self.search_button = Button(top, text="Search", command=self.cleanup, bg="white")
		self.search_button.grid(row=3, column=3)

	def change_search_type(self, first_time):
		"""
		Changes the search type from address-based to coordinate-based or the other way around.
		:param first_time: A flag indicating whether this is the first time the type button is pressed
		:return: None
		"""

		if self.latitude["information_general"] == "Latitude:":
			self.latitude["information_general"] = "Address:"
			self.long_entry.grid_forget()
			self.type_button.configure(text="Coordinates")
			self.longitude["information_general"] = ""
			first_time = False

		if self.latitude["information_general"] == "Address:" and first_time:
			self.latitude.config(text="Latitude:")
			self.long_entry.grid(row=2, column=3)
			self.type_button.configure(text="Address")
			self.longitude["information_general"] = "Longitude:"

	def cleanup(self):
		"""
		Makes the location-type request and cleans up after itself by tearing down the GUI and
		effectively returning control to the main screen.
		:return: None
		"""

		list_entries = [
			self.lat_entry,
			self.long_entry,
		]
		wrong_counter_list = []

		for counter, element in enumerate(list_entries, 0):
			if InputUtil.is_float(element.get()) is False:
				wrong_counter_list.append(counter)

		if len(wrong_counter_list) > 0:
			messagebox.showinfo("Input Error", "All entries must be filled out with correct coordinates")
			for number in wrong_counter_list:
				list_entries[number].delete(0, 'end')

		else:
			self.value = [float(self.lat_entry.get()), float(self.long_entry.get())]

			temp_window = PreviewWindow(
				main_screen=self.main_screen,
				master=self.master,
				application=self.application,
				coordinates=self.value
			)
			self.top.destroy()
			self.main_screen.master.wait_window(temp_window.top)
