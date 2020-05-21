from tkinter import Button, Entry, Label, Toplevel

from mesh_city.user.entities.image_provider_entity import ImageProviderEntity
from mesh_city.user.entities.user_entity import UserEntity


class CreateNewUserWindow:

	def __init__(self, master, application):
		self.value = ""
		self.master = master
		self.application = application
		top = self.top = Toplevel(master)
		self.geometry = "200x200"

		self.top_label = Label(top, text="Please insert your information")
		self.top_label.grid(row=0, columnspan=3)
		self.name_label = Label(top, text="Name")
		self.name_label.grid(row=1, column=0)
		self.name_entry = Entry(top)
		self.name_entry.grid(row=1, column=1, columnspan=2)

		self.select_image_provider = Label(top, text="Please select an image provider")
		self.select_image_provider.grid(row=2, columnspan=3)
		self.google_maps_button = Button(top, text="Google Maps", command=self.google_maps)
		self.google_maps_button.grid(row=3, column=1)

		self.confirm_button = Button(self.top, text="Confirm", command=self.cleanup)

		self.end = 3
		self.count = 1
		self.map_providers = []
		self.map_providers_size = -1

	def google_maps(self):

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

	def cleanup(self):

		image_provider_entity_dic = {}

		temp_counter = 1
		for x in range(0, self.map_providers_size, 2):
			temp_api_key = self.map_providers[x].get()
			x += 1
			temp_quota = self.map_providers[x].get()
			x += 1
			temp_name = "Google Maps " + str(temp_counter)
			image_provider_entity_dic[temp_name] = ImageProviderEntity(
				file_handler=self.application.file_handler,
				type="google_maps",
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

		self.application.late_init(new_user)
		self.top.destroy()
