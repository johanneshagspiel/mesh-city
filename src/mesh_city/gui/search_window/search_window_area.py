"""
See :class:`.SearchWindowLocationArea`
"""

from tkinter import Button, Entry, Label, messagebox, Toplevel

from mesh_city.gui.search_window.preview_window import PreviewWindow
from mesh_city.util.input_util import InputUtil


class SearchWindowLocationArea:
	"""
	A pop-up type GUI element that the user can fill in to make an area-type request.
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

		Label(top, text="Which area are you interested in downloading ?").grid(row=0, column=3)

		self.min_lat = Label(top, text="Min Latitude:")
		self.min_lat.grid(row=1, column=1)
		self.min_log = Label(top, text="Min Longitude:")
		self.min_log.grid(row=2, column=1)
		self.max_lat = Label(top, text="Max Latitude:")
		self.max_lat.grid(row=3, column=1)
		self.max_log = Label(top, text="Max Longitude:")
		self.max_log.grid(row=4, column=1)

		self.min_lat_entry = Entry(top, width=20)
		self.min_lat_entry.grid(row=1, column=3)
		self.min_long_entry = Entry(top, width=20)
		self.min_long_entry.grid(row=2, column=3)
		self.max_lat_entry = Entry(top, width=20)
		self.max_lat_entry.grid(row=3, column=3)
		self.max_long_entry = Entry(top, width=20)
		self.max_long_entry.grid(row=4, column=3)

		Button(top, text="Search", command=self.cleanup, bg="white").grid(row=5, column=3)

	def cleanup(self):
		"""
		Makes the area-type request and cleans up after itself by tearing down the GUI and
		effectively returning control to the main screen.
		"""
		list_entries = [
			self.min_lat_entry, self.min_long_entry, self.max_lat_entry, self.max_long_entry,
		]
		wrong_counter_list = []

		for counter, element in enumerate(list_entries, 0):
			if InputUtil.is_float(element.get()) is False:
				wrong_counter_list.append(counter)

		if len(wrong_counter_list) > 0:
			messagebox.showinfo(
				"Input Error", "All entries must be filled out with correct coordinates"
			)
			for number in wrong_counter_list:
				list_entries[number].delete(0, 'end')

		else:
			self.value = [
				float(self.min_lat_entry.get()),
				float(self.min_long_entry.get()),
				float(self.max_lat_entry.get()),
				float(self.max_long_entry.get()),
			]

			temp_window = PreviewWindow(
				main_screen=self.main_screen,
				master=self.master,
				application=self.application,
				coordinates=self.value
			)
			self.top.destroy()
			self.main_screen.master.wait_window(temp_window.top)
