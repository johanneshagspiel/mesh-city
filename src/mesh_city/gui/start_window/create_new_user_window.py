"""
A module containing the create new user window
"""
from tkinter import Button, Entry, Label, Toplevel, messagebox

from mesh_city.logs.log_entities.coordinate_overview import CoordinateOverview
from mesh_city.user.entities.image_provider_entity import ImageProviderEntity
from mesh_city.user.entities.user_entity import UserEntity
from mesh_city.util.input_util import InputUtil


# TODO check user input (check that google maps api key is an google maps api key)
class CreateNewUserWindow:
	"""
	The create new user window class is where a new user can enter their information to make a new
	account which is stored in a json file
	"""

	def __init__(self, master, application):
		"""
		First the user is asked for their name, then they can add as many google maps api accounts
		as they want
		:param master: the master tkinter object
		:param application: the global application context
		"""
		self.value = ""
		self.master = master
		self.application = application
		top = self.top = Toplevel(master)
		self.geometry = "200x200"

		self.top.config(padx=4)
		self.top.config(pady=4)

		self.top_label = Label(top, text="Please insert your information")
		self.top_label.grid(row=0, columnspan=3)
		self.name_label = Label(top, text="Name")
		self.name_label.grid(row=1, column=0, sticky="w")
		self.name_entry = Entry(top)
		self.name_entry.grid(row=1, column=1, columnspan=2)

		self.provider_number = 0

		self.select_image_provider = Label(top, text="Please select an image provider")
		self.select_image_provider.grid(row=2, columnspan=3)
		self.google_maps_button = Button(
			top, text="Google Maps", command=self.google_maps, bg="white"
		)
		self.google_maps_button.grid(row=3, column=1)

		self.confirm_button = Button(self.top, text="Confirm", command=self.cleanup, bg="white")

		self.end = 3
		self.count = 1
		self.map_providers = []
		self.map_providers_size = -1

	# pylint: disable=W0201
	def google_maps(self):
		"""
		Creates additional buttons if the user wants to add another google maps account
		:return: nothing
		"""
		self.provider_number += 1
		temp_name = str("Google Maps ") + str(self.count)
		self.count += 1
		self.temp_name_label = Label(self.top, text=temp_name)
		self.temp_name_label.grid(row=self.end, column=0, sticky="w")
		self.end += 1

		self.api_key = Label(self.top, text="API Key")
		self.api_key.grid(row=self.end, column=0, sticky="w")

		self.map_providers.append(Entry(self.top))
		self.map_providers_size += 1
		self.map_providers[self.map_providers_size].grid(row=self.end, column=1, columnspan=2)
		self.end += 1

		self.quota = Label(self.top, text="Monthly Quota")
		self.quota.grid(row=self.end, column=0, sticky="w")

		self.map_providers.append(Entry(self.top))
		self.map_providers_size += 1
		self.map_providers[self.map_providers_size].grid(row=self.end, column=1, columnspan=2)
		self.end += 1

		if self.provider_number < 5:
			self.select_image_provider.grid(row=self.end, columnspan=3)
			self.end += 1
			self.google_maps_button.grid(row=self.end, column=1)
			self.end += 1
		else:
			self.select_image_provider.grid_forget()
			self.google_maps_button.grid_forget()

		self.confirm_button.grid(row=self.end, column=1)

	def cleanup(self):
		"""
		The method called when the user clicks on the confirm button. Creates a new user with the
		provided information, saves that to json and loads the main_screen
		:return: nothing
		"""

		wrong_entry_list = []

		for counter, entry in enumerate(self.map_providers):
			if counter == 0 or counter % 2 == 0:
				if InputUtil.is_google_api(entry.get()) is False:
					wrong_entry_list.append(counter)
			if counter % 2 == 1:
				if InputUtil.is_float(entry.get()) is False:
					wrong_entry_list.append(counter)

		if len(wrong_entry_list) > 0 or self.name_entry.get() == "":
			messagebox.showinfo("Input Error", "All entries must be filled out with correct information\nAPI keys must start with 'AIza'")
			for number in wrong_entry_list:
				self.map_providers[number].delete(0, 'end')

		else:
			image_provider_entity_dic = {}

			temp_counter = 1
			for number in range(0, self.map_providers_size, 2):
				temp_api_key = self.map_providers[number].get()
				number += 1
				temp_quota = self.map_providers[number].get()
				number += 1
				temp_name = "Google Maps " + str(temp_counter)
				image_provider_entity_dic[temp_name] = ImageProviderEntity(
					file_handler=self.application.file_handler,
					type_map_provider="Google Maps",
					api_key=temp_api_key,
					quota=temp_quota
				)
				temp_counter += 1

			name = self.name_entry.get()
			new_user = UserEntity(
				file_handler=self.application.file_handler,
				name=name,
				image_providers=image_provider_entity_dic
			)
			self.application.log_manager.write_log(new_user)

		self.application.set_user_entity(new_user)

		self.top.destroy()
