from tkinter import Button, END, Label, Toplevel, Text, CHAR, Entry


class UserWindow:

	def __init__(self, master, application, main_screen):
		"""
		The user is shown an overview over their map providers
		:param master: the master tkinter object
		:param application: the global application context
		:param main_screen: the main screen of the application
		"""
		self.main_screen = main_screen
		self.master = master
		self.application = application
		self.main_screen = main_screen
		self.top = Toplevel(master)

		self.user_entity = self.application.user_entity
		self.pot_delete_list = []
		self.end = 1
		self.map_providers = []
		self.map_providers_size = -1

		self.name_label = Label(self.top, text=self.user_entity.name)
		self.name_label.grid(row=0, columnspan=2)
		self.pot_delete_list.append(self.name_label)

		self.change_name_button = Button(self.top, text="Change name", command=self.change_name, bg="white")
		self.change_name_button.grid(row=1, columnspan=2)
		self.pot_delete_list.append(self.change_name_button)

		self.top_label = Label(self.top, text="\nYour image providers:")
		self.top_label.grid(row=2, columnspan=2)

		counter = 3
		self.count = 0
		for name, image_provider in self.user_entity.image_providers.items():
			self.count += 1

			self.temp_name_label = Label(self.top, text=name)
			self.temp_name_label.grid(row=counter, column=0, sticky="w")
			self.pot_delete_list.append(self.temp_name_label)
			counter += 1

			temp_api_text = "API Key: "
			self.temp_api_label = Label(self.top, text=temp_api_text)
			self.temp_api_label.grid(row=counter, column=0, sticky="w")
			self.pot_delete_list.append(self.temp_api_label)

			self.api_key_text = Text(self.top, width=20, height=2, wrap=CHAR)
			self.api_key_text.grid(row=counter, column=1)
			self.api_key_text.configure(font=("TkDefaultFont", 9, "normal"))
			self.api_key_text.insert(END, image_provider.api_key)
			self.api_key_text.configure(state='disabled')
			self.pot_delete_list.append(self.api_key_text)
			counter += 1

			temp_usage_text = "Usage: " + str(image_provider.usage["static_map"])
			self.temp_usage_label = Label(self.top, text=temp_usage_text)
			self.temp_usage_label.grid(row=counter, column=0, sticky="w")
			self.pot_delete_list.append(self.temp_usage_label)
			counter += 1

			temp_quota_text = "Quota: " + str(image_provider.quota)
			self.temp_quota_label = Label(self.top, text=temp_quota_text)
			self.temp_quota_label.grid(row=counter, column=0, sticky="w")
			self.pot_delete_list.append(self.temp_quota_label)
			self.change_quota_button = Button(self.top, text="Change quota",
			                                  command=lambda : self.change_quota(name),
			                                  bg="white")
			self.change_quota_button.grid(row=counter, column=1)
			self.pot_delete_list.append(self.change_quota_button)
			counter += 1

			temp_date_reset_text = "Date Quota Reset: " + str(image_provider.date_reset) + "\n"
			self.temp_date_reset_label = Label(self.top, text=temp_date_reset_text)
			self.temp_date_reset_label.grid(row=counter, columnspan=2, sticky="w")
			self.pot_delete_list.append(self.temp_date_reset_label)
			counter += 1

		self.additional_provider_button = Button(
			self.top, text="Add new image provider", command=self.add_provider, bg="white")
		self.additional_provider_button.grid(row=counter, columnspan=2)
		self.pot_delete_list.append(self.additional_provider_button)


	def add_provider(self):
		self.top_label["text"] = "Test"

		for element in self.pot_delete_list:
			element.grid_forget()

		temp_name = str("Google Maps ") + str(self.count)
		self.count += 1
		self.temp_name_label = Label(self.top, text=temp_name)
		self.temp_name_label.grid(row=self.end, column=0)
		self.end += 1

		self.api_key = Label(self.top, text="API Key")
		self.api_key.grid(row=self.end, column=0)

		self.map_providers.append(Entry(self.top))
		self.map_providers_size += 1
		self.map_providers[self.map_providers_size].grid(row=self.end, column=1, columnspan=2)
		self.end += 1

		self.quota = Label(self.top, text="Monthly Quota")
		self.quota.grid(row=self.end, column=0)

		self.map_providers.append(Entry(self.top))
		self.map_providers_size += 1
		self.map_providers[self.map_providers_size].grid(row=self.end, column=1, columnspan=2)
		self.end += 1

		self.select_image_provider.grid(row=self.end, columnspan=3)
		self.end += 1
		self.google_maps_button.grid(row=self.end, column=1)
		self.end += 1

		self.confirm_button.grid(row=self.end, column=1)

	def change_quota(self, name):
		print(name)

	def change_name(self):
		return None
