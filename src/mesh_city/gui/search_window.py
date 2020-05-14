from pathlib import Path
from tkinter import Button, Entry, Label, Toplevel

class SearchWindowStart(object):

	def __init__(self, master, application, mainscreen):
		self.mainscreen = mainscreen
		self.master = master
		self.value = ""
		self.application = application
		top = self.top = Toplevel(master)

		Label(top,
		      text="What kind of search are you interested in ?").grid(
			row=0, columnspan=3
		)

		self.button_area = Button(top, text="Area", command=self.button_area).grid(row=1, columnspan=1)
		self.button_location = Button(top, text="Location", command=self.button_location).grid(row=1, columnspan=3)

	def button_area(self):
		SearchWindowLocationArea(self.master, self.application, self.mainscreen)
		self.top.destroy()

	def button_location(self):
		SearchWindowLocation(self.master, self.application, self.mainscreen)
		self.top.destroy()

class SearchWindowLocation(object):

	def __init__(self, master, application, mainscreen):
		self.mainscreen = mainscreen
		self.master = master
		self.value = ""
		self.application = application
		top = self.top = Toplevel(master)

		Label(top,
			text="Which location are you interested in downloading ?").grid(
			row=0, column=3
			)

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
		self.address_info_2 = Label(self.top, text="{house number} {street} {postcode} {city} {country}")
		self.address_info_2.grid(row=4, column=4)

		self.search_button = Button(top, text="Search", command=self.cleanup)
		self.search_button.grid(row=3, column=3)
		self.type_button = Button(top, text="Address", command=lambda : self.change_search_type(True))
		self.type_button.grid(row=1, column=4)

	def change_search_type(self, firstTime):
		if(self.latitude['text'] == "Latitude:"):
			self.latitude['text'] ="Address:"
			self.long_entry.grid_forget()
			self.type_button.configure(text="Coordinates")
			self.longitude['text'] = ""
			firstTime = False

		if((self.latitude['text'] == "Address:") & (firstTime == True)):
			self.latitude.config(text="Latitude:")
			self.long_entry.grid(row=2, column=3)
			self.type_button.configure(text="Address")
			self.longitude['text'] = "Longitude:"

	def cleanup(self):
		self.value = [float(self.lat_entry.get()), float(self.long_entry.get())]
		self.application.request_manager.make_request_for_block(self.value)
		self.mainscreen.currently_active_image = self.application.request_manager.path_to_map_image
		self.mainscreen.currently_active_request = Path(self.mainscreen.currently_active_image).parents[0]
		self.mainscreen.update_Image()
		self.top.destroy()

class SearchWindowLocationArea(object):

	def __init__(self, master, application, mainscreen):
		self.mainscreen = mainscreen
		self.master = master
		self.value = ""
		self.application = application
		top = self.top = Toplevel(master)

		Label(top,
			text="Which area are you interested in downloading ?").grid(
			row=0, column=3
			)

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

		self.type_button_min = Button(top, text="Address", command=lambda : self.change_search_type(True, "min"))
		self.type_button_min.grid(row=1, column=4)

		self.type_button_max = Button(top, text="Address", command=lambda : self.change_search_type(True, "max"))
		self.type_button_max.grid(row=3, column=4)

	def change_search_type(self, firstTime, name):
		if(name == "min"):
			if(self.min_lat['text'] == "Min Latitude:"):
				self.min_lat['text'] ="Address:"
				self.min_long_entry.grid_forget()
				self.type_button_min.configure(text="Coordinates")
				self.min_log['text'] = ""
				firstTime = False

			if((self.min_lat['text'] == "Address:") & (firstTime == True)):
				self.min_lat['text'] = "Min Latitude:"
				self.min_long_entry.grid(row=2, column=3)
				self.type_button_min.configure(text="Address")
				self.min_log['text'] = "Min Longitude:"

		if(name == "max"):
			if(self.max_lat['text'] == "Max Latitude:"):
				self.max_lat['text'] ="Address:"
				self.max_long_entry.grid_forget()
				self.type_button_max.configure(text="Coordinates")
				self.max_log['text'] = ""
				firstTime = False

			if((self.max_lat['text'] == "Address:") & (firstTime == True)):
				self.max_lat['text'] = "Max Latitude:"
				self.max_long_entry.grid(row=2, column=3)
				self.type_button_max.configure(text="Address")
				self.max_log['text'] = "Max Longitude:"

	def cleanup(self):
		self.value = [float(self.min_lat_entry.get()), float(self.min_long_entry.get()),
		              float(self.max_lat_entry.get()), float(self.max_long_entry.get())]
		self.application.request_manager.make_request_for_block(self.value)
		self.mainscreen.currently_active_image = self.application.request_manager.path_to_map_image
		self.mainscreen.currently_active_request = Path(self.mainscreen.currently_active_image).parents[0]
		self.mainscreen.update_Image()
		self.top.destroy()
