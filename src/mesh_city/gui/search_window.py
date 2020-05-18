"""This module manages the making of two types of imagery requests,
requests for a rectangular area and requests for points on the map"""
from pathlib import Path
from tkinter import Button, Entry, Label, Toplevel


class SearchWindowStart:
	"""
	This class is a GUI element that provides the user with the type of pop-up they need to make the
	request they want to make after the request type is selected.
	"""
	def __init__(self, master, application, main_screen):
		"""
		Initializes the GUI elements for a window and prompts the user to enter what type of search
		they are interested in.
		:param master: The Tk root.
		:param application: The application object that is used to make requests.
		:param main_screen: The main screen object the popups can interact with.
		"""
		self.main_screen = main_screen
		self.master = master
		self.value = ""
		self.application = application
		self.top = Toplevel(master)
		Label(self.top, text="What kind of search are you interested in ?").grid(row=0, columnspan=3)
		Button(self.top, text="Area",
			command=self.button_area_callback).grid(row=1, columnspan=1)
		Button(self.top, text="Location",
			command=self.button_location_callback).grid(row=1, columnspan=3)

	def button_area_callback(self):
		"""
		Creates an area-type pop-up that in the end makes the area request to the backend.
		:return: None
		"""
		SearchWindowLocationArea(self.master, self.application, self.main_screen)
		self.top.destroy()

	def button_location_callback(self):
		"""
		Creates an location-type pop-up that in the end makes the location request to the backend.
		:return: None
		"""
		SearchWindowLocation(self.master, self.application, self.main_screen)
		self.top.destroy()


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

		Label(top, text="Which location are you interested in downloading ?").grid(row=0, column=3)

		self.latitude = Label(top, text="Latitude:")
		self.latitude.grid(row=1, column=1)
		self.longitude = Label(top, text="Longitude:")
		self.longitude.grid(row=2, column=1)

		self.lat_entry = Entry(top, width=20)
		self.lat_entry.grid(row=1, column=3)
		self.long_entry = Entry(top, width=20)
		self.long_entry.grid(row=2, column=3)

		self.address_info_1 = Label(self.top, text="Please enter the address in this form:")
		self.address_info_1.grid(row=3, column=4)
		self.address_info_2 = Label(
			self.top, text="{house number} {street} {postcode} {city} {country}"
		)
		self.address_info_2.grid(row=4, column=4)

		self.search_button = Button(top, text="Search", command=self.cleanup)
		self.search_button.grid(row=3, column=3)
		self.type_button = Button(
			top, text="Address", command=lambda: self.change_search_type(True)
		)
		self.type_button.grid(row=1, column=4)

	def change_search_type(self, first_time):
		"""
		Changes the search type from address-based to coordinate-based or the other way around.
		:param first_time: A flag indicating whether this is the first time the type button is pressed
		:return: None
		"""
		if self.latitude['text'] == "Latitude:":
			self.latitude['text'] = "Address:"
			self.long_entry.grid_forget()
			self.type_button.configure(text="Coordinates")
			self.longitude['text'] = ""
			first_time = False

		if (self.latitude['text'] == "Address:") & first_time:
			self.latitude.config(text="Latitude:")
			self.long_entry.grid(row=2, column=3)
			self.type_button.configure(text="Address")
			self.longitude['text'] = "Longitude:"

	def cleanup(self):
		"""
		Makes the location-type request and cleans up after itself by tearing down the GUI and
		effectively returning control to the main screen.
		:return: None
		"""
		self.value = [float(self.lat_entry.get()), float(self.long_entry.get())]
		self.application.request_manager.make_request_for_block(self.value)
		self.main_screen.currently_active_tile = self.application.request_manager.active_tile_path
		self.main_screen.currently_active_request = Path(self.main_screen.currently_active_tile
														).parents[0]
		self.main_screen.update_image()
		self.top.destroy()


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

		self.temp_1 = Label(self.top, text="Please enter address information in this form:")
		self.temp_1.grid(row=5, column=4)
		self.temp_2 = Label(self.top, text="{house number} {street} {postcode} {city} {country}")
		self.temp_2.grid(row=6, column=4)

		Button(top, text="Search", command=self.cleanup).grid(row=5, column=3)

		self.type_button_min = Button(
			top, text="Address", command=lambda: self.change_search_type(True, "min")
		)
		self.type_button_min.grid(row=1, column=4)

		self.type_button_max = Button(
			top, text="Address", command=lambda: self.change_search_type(True, "max")
		)
		self.type_button_max.grid(row=3, column=4)

	def change_search_type(self, first_time, name):
		"""
		Changes the search type from address-based to coordinate-based or the other way around.
		:param first_time: A flag indicating whether this is the first time the type button is pressed
		:param name: The name indicating which of the points of the rectangle-defined area is to
		have a different type.
		:return:
		"""
		if name == "min":
			if self.min_lat['text'] == "Min Latitude:":
				self.min_lat['text'] = "Address:"
				self.min_long_entry.grid_forget()
				self.type_button_min.configure(text="Coordinates")
				self.min_log['text'] = ""
				first_time = False

			if (self.min_lat['text'] == "Address:") & first_time:
				self.min_lat['text'] = "Min Latitude:"
				self.min_long_entry.grid(row=2, column=3)
				self.type_button_min.configure(text="Address")
				self.min_log['text'] = "Min Longitude:"

		if name == "max":
			if self.max_lat['text'] == "Max Latitude:":
				self.max_lat['text'] = "Address:"
				self.max_long_entry.grid_forget()
				self.type_button_max.configure(text="Coordinates")
				self.max_log['text'] = ""
				first_time = False

			if (self.max_lat['text'] == "Address:") & first_time:
				self.max_lat['text'] = "Max Latitude:"
				self.max_long_entry.grid(row=4, column=3)
				self.type_button_max.configure(text="Address")
				self.max_log['text'] = "Max Longitude:"

	def cleanup(self):
		"""
		Makes the area-type request and cleans up after itself by tearing down the GUI and
		effectively returning control to the main screen.
		"""
		self.value = [
			float(self.min_lat_entry.get()),
			float(self.min_long_entry.get()),
			float(self.max_lat_entry.get()),
			float(self.max_long_entry.get())
		]
		self.application.request_manager.make_request_for_block(self.value)
		self.main_screen.currently_active_tile = self.application.request_manager.active_tile_path
		self.main_screen.currently_active_request = Path(self.main_screen.currently_active_tile
														).parents[0]
		self.main_screen.update_image()
		self.top.destroy()
