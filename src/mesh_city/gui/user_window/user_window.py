from tkinter import Button, END, Label, Toplevel, Text, CHAR, Entry

from mesh_city.user.entities.image_provider_entity import ImageProviderEntity


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

		self.top.config(padx=4)
		self.top.config(pady=4)

		self.user_entity = self.application.user_entity
		self.pot_delete_list = []
		self.end = 1
		self.map_providers = []
		self.map_providers_size = -1

		self.google_maps_button = Button(
			self.top, text="Add another provider", command=self.add_another_provider, bg="white"
		)
		self.confirm_button = Button(self.top, text="Confirm", command=self.add_providers, bg="white")

		self.name_label = Label(self.top, text=self.user_entity.name)
		self.name_label.grid(row=0, columnspan=2)
		self.pot_delete_list.append(self.name_label)

		self.change_name_button = Button(self.top, text="Change name", command=self.change_name, bg="white")
		self.change_name_button.grid(row=1, columnspan=2)
		self.pot_delete_list.append(self.change_name_button)
		self.provider_number = 0

		temp_text = "\nYour image provider:"
		if len(self.user_entity.image_providers.keys()) > 1:
			temp_text = "\nYour image providers:"
		self.top_label = Label(self.top, text=temp_text)
		self.top_label.grid(row=2, columnspan=2)

		counter = 3
		self.count = 1
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

			self.temp_usage_label = Label(self.top, text="Usage: ")
			self.temp_usage_label.grid(row=counter, column=0, sticky="w")
			self.pot_delete_list.append(self.temp_usage_label)

			self.temp_usage_label_amount = Label(self.top, text=str(image_provider.usage["static_map"]))
			self.temp_usage_label_amount.grid(row=counter, column=1, sticky="w")
			self.pot_delete_list.append(self.temp_usage_label_amount)
			counter += 1

			self.temp_quota_label = Label(self.top, text="Quota: ")
			self.temp_quota_label.grid(row=counter, column=0, sticky="w")
			self.pot_delete_list.append(self.temp_quota_label)

			self.temp_quota_label_amount = Label(self.top, text=str(image_provider.quota))
			self.temp_quota_label_amount.grid(row=counter, column=1, sticky="w")
			self.pot_delete_list.append(self.temp_quota_label_amount)
			counter += 1

			self.change_quota_button = Button(self.top, text="Change quota",
			                                  command=lambda : self.change_quota(str(image_provider.quota),
			                                                                     str(image_provider.usage["static_map"]),
			                                                                     name),
			                                  bg="white")
			self.change_quota_button.grid(row=counter, columnspan=2)
			self.pot_delete_list.append(self.change_quota_button)
			counter += 1

			self.temp_date_reset_label = Label(self.top, text="Date Quota Reset: \n")
			self.temp_date_reset_label.grid(row=counter, column=0, sticky="w")
			self.pot_delete_list.append(self.temp_date_reset_label)

			self.temp_date_reset_label_amount = Label(self.top, text=str(image_provider.date_reset) + "\n")
			self.temp_date_reset_label_amount.grid(row=counter, column=1, sticky="w")
			self.pot_delete_list.append(self.temp_date_reset_label_amount)
			counter += 1
			self.provider_number += 1

		self.provider_number_start = self.provider_number

		self.additional_provider_button = Button(
			self.top, text="Add new image provider", command=self.add_another_provider, bg="white")
		self.additional_provider_button.grid(row=counter, columnspan=2)
		self.pot_delete_list.append(self.additional_provider_button)


	def add_another_provider(self):
		self.provider_number += 1

		self.top_label["text"] = "Please fill in all the fields"
		self.top_label.grid(row=0)

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

		if self.provider_number < 5:
			self.google_maps_button.grid(row=self.end, column=1)
			self.end += 1
		else:
			self.google_maps_button.grid_forget()

		self.confirm_button.grid(row=self.end, column=1)

	def change_quota(self, old_quota, usage, name):
		for element in self.pot_delete_list:
			element.grid_forget()
		self.top_label.grid_forget()

		temp_old_quota = Label(self.top, text="Old Quota: ")
		temp_old_quota.grid(row=0, column=0, sticky="w")

		temp_old_quota_amount = Label(self.top, text=old_quota)
		temp_old_quota_amount.grid(row=0, column=1)

		temp_current_usage = Label(self.top, text="Current Usage: ")
		temp_current_usage.grid(row=1, column=0, sticky="w")

		temp_current_usage_amount = Label(self.top, text=usage)
		temp_current_usage_amount.grid(row=1, column=1)

		temp_new_quota = Label(self.top, text="New Quota: ")
		temp_new_quota.grid(row=2, column=0,  sticky="w")

		temp_new_quota_entry = Entry(self.top)
		temp_new_quota_entry.grid(row=2, column=1)

		temp_new_quota_button = Button(self.top, text="Confirm",
		                              command=lambda : self.change_quota_confirm(temp_new_quota_entry.get(), name), bg="white")
		temp_new_quota_button.grid(row=3, columnspan=2)

	def change_quota_confirm(self, new_quota, name):
		self.user_entity.image_providers[name].quota = new_quota
		self.application.log_manager.write_log(self.user_entity)
		self.top.destroy()

	def change_name(self):
		for element in self.pot_delete_list:
			element.grid_forget()
		self.top_label.grid_forget()

		temp_new_name = Label(self.top, text="New Name: ")
		temp_new_name.grid(row=0, column=0)

		temp_new_name_entry = Entry(self.top)
		temp_new_name_entry.grid(row=0, column=1)

		temp_new_name_button = Button(self.top, text="Confirm",
		                              command=lambda : self.change_name_confirm(temp_new_name_entry.get()), bg="white")
		temp_new_name_button.grid(row=1, columnspan=2)

	def change_name_confirm(self, new_name):
		self.application.log_manager.change_name(self.user_entity.name, new_name)
		self.user_entity.name = new_name
		self.top.destroy()

	def add_providers(self):

		image_provider_entity_dic = {}

		temp_counter = self.provider_number_start + 1
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

		for name, value in image_provider_entity_dic.items():
			self.user_entity.image_providers[name] = value

		self.application.log_manager.write_log(self.user_entity)
		self.top.destroy()
