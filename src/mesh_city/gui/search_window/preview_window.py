"""
A module containing the preview window
"""
from tkinter import Button, Entry, Label, Toplevel

from mesh_city.user.image_provider_entity import ImageProviderEntity
from mesh_city.util.price_table_util import PriceTableUtil


# pylint: disable=W0201
class PreviewWindow:
	"""
	The preview window class is the gui element that shows the user how much a request would cost
	and lets the user decide which map provider to use to make a request
	"""

	# TODO change the gui to checkboxes
	def __init__(self, master, application, main_screen, coordinates):
		"""
		The initialization method: first asks the user which map provider to use for the request,
		based on which it then calculates how much money the request would cost
		:param master: the master tkinter object
		:param application: the global application context
		:param main_screen: the main screen of the application
		:param coordinates: the tile_information of the request
		"""
		self.main_screen = main_screen
		self.master = master
		self.coordinates = coordinates
		self.application = application
		self.user_entity = self.application.user_entity
		top = self.top = Toplevel(master)

		self.top.config(padx=4)
		self.top.config(pady=4)

		self.top_label = Label(top, text="Which image provider do you want to use?")
		self.top_label.grid(row=0, columnspan=2)

		self.count = 2
		self.provider_number = 0

		self.temp_list = []
		self.temp_list_size = -1

		self.chosen_list = []
		self.list_providers = []

		for key, value in self.application.user_entity.image_providers.items():
			self.provider_number += 1
			self.temp_list.append(
				Button(
				self.top,
				text=key,
				command=lambda value=value: self.calculate_locations(key, value),
				bg="white"
				)
			)
			self.temp_list_size += 1
			self.temp_list[self.temp_list_size].grid(row=self.count, column=0)

			temp_text = "Usage left: " + str(
				round((float(value.quota) - float(value.usage["total"])), 4)
			)
			self.temp_list.append(Label(self.top, text=temp_text))
			self.temp_list_size += 1
			self.temp_list[self.temp_list_size].grid(row=self.count, column=1)
			self.count += 1

		self.additional_provider_button = Button(
			self.top, text="Add new image provider", command=self.add_another_provider, bg="white"
		)
		self.temp_list.append(self.additional_provider_button)
		self.additional_provider_button.grid(row=self.count, columnspan=2)

	def add_another_provider(self) -> None:
		"""
		Adds a new provider object.
		:return: None
		"""

		self.addition_provider_gui_list = []

		self.provider_number += 1
		self.count += 1

		temp_name = str("Google Maps ") + str(self.provider_number)
		self.provider_number += 1
		self.temp_name_label = Label(self.top, text=temp_name)
		self.temp_name_label.grid(row=self.count, column=0)
		self.temp_list.append(self.temp_name_label)
		self.addition_provider_gui_list.append(self.temp_name_label)
		self.count += 1

		self.api_key = Label(self.top, text="API Key")
		self.api_key.grid(row=self.count, column=0)
		self.temp_list.append(self.api_key)
		self.addition_provider_gui_list.append(self.api_key)

		self.api_key_entry = Entry(self.top)
		self.api_key_entry.grid(row=self.count, column=1, columnspan=2)
		self.temp_list.append(self.api_key_entry)
		self.addition_provider_gui_list.append(self.api_key_entry)
		self.count += 1

		self.quota = Label(self.top, text="Monthly Quota")
		self.quota.grid(row=self.count, column=0)
		self.temp_list.append(self.quota)
		self.addition_provider_gui_list.append(self.quota)

		self.quota_entry = Entry(self.top)
		self.quota_entry.grid(row=self.count, column=1, columnspan=2)
		self.temp_list.append(self.quota_entry)
		self.addition_provider_gui_list.append(self.quota_entry)
		self.count += 1

		self.confirm_button = Button(self.top, text="Confirm", command=None)
		self.confirm_button = Button(
			self.top, text="Confirm", command=self.confirm_additional_provider
		)
		self.confirm_button.grid(row=self.count, column=1)
		self.temp_list.append(self.confirm_button)
		self.addition_provider_gui_list.append(self.confirm_button)

		self.additional_provider_button.grid_forget()

	def calculate_locations(
		self, image_provider_entity_name: str, image_provider_entity: ImageProviderEntity
	) -> None:
		"""
		Calculates the number of requests that will have to be made for these coordinates.
		:param image_provider_entity_name: The name of the ImageProviderEntity
		:param image_provider_entity: The ImageProviderEntity
		:return: None
		"""
		self.application.request_maker.top_down_provider = image_provider_entity.top_down_provider
		self.application.request_maker.image_provider = image_provider_entity
		# this is a location request
		locations = []
		if len(self.coordinates) == 2:
			locations, _, _ = self.application.request_maker.calculate_coordinates_for_location(
				latitude=self.coordinates[0], longitude=self.coordinates[1])
		elif len(self.coordinates) == 4:
			# makes sure that points are always at least a little bit apart
			self.coordinates[2] += 0.0005
			self.coordinates[3] += 0.0005
			locations, _, _ = self.application.request_maker.calculate_coordinates_for_rectangle(
				bottom_latitude=self.coordinates[0], left_longitude=self.coordinates[1],
				top_latitude=self.coordinates[2], right_longitude=self.coordinates[3])

		self.number_requests = self.application.request_maker.count_uncached_tiles(locations)
		self.check_usage(image_provider_entity_name, image_provider_entity)

	def check_usage(
		self, image_provider_entity_name: str, image_provider_entity: ImageProviderEntity
	) -> None:
		"""
		Method to check how much this request would cost
		:param image_provider_entity: the image provider entity used for the request
		:return: nothing (updates the gui to show how much the request would cost)
		"""
		self.chosen_list.append(image_provider_entity_name)

		for widget in self.temp_list:
			widget.grid_forget()

		temp_cost = PriceTableUtil.calculate_action_price(
			image_provider_entity.type,
			"static_map",
			self.number_requests,
			image_provider_entity.quota,
			image_provider_entity.usage["total"]
		)

		if temp_cost[0] != -1:
			self.list_providers.append(
				(image_provider_entity_name, temp_cost[0], temp_cost[1], temp_cost[2])
			)
			self.confirm_download()
		else:
			self.number_requests -= temp_cost[2]
			self.list_providers.append(
				(image_provider_entity_name, temp_cost[1], temp_cost[2], temp_cost[3])
			)
			self.select_additional_providers()

	def select_additional_providers(self) -> None:
		"""
		Prompts the user to select additional providers for requests that would exceed the quota
		:return: None
		"""
		for widget in self.temp_list:
			widget.grid_forget()

		self.top_label.configure(text="Using only this image provider would exceed its quota.")

		number_requests_label_text = "Images still to be downloaded: " + str(self.number_requests)
		self.number_requests_label = Label(self.top, text=str(number_requests_label_text))
		self.number_requests_label.grid(row=1, column=0)

		self.count = 2

		for key, value in self.application.user_entity.image_providers.items():
			if key not in self.chosen_list:
				self.provider_number += 1
				self.temp_button = Button(
					self.top,
					text=key,
					command=lambda value=value,
					key=key: self.check_usage(key, value),
					bg="white"
				)
				self.temp_button.grid(row=self.count, column=0)
				self.temp_list.append(self.temp_button)

				temp_text = "Usage left: " + str(
					round((float(value.quota) - float(value.usage["total"])), 4)
				)
				self.temp_label = Label(self.top, text=temp_text)
				self.temp_label.grid(row=self.count, column=1)
				self.temp_list.append(self.temp_label)
				self.count += 1

		self.additional_provider_button = Button(
			self.top, text="Add new image provider", command=self.add_another_provider, bg="white"
		)
		self.temp_list.append(self.additional_provider_button)
		self.additional_provider_button.grid(row=self.count, column=0, columnspan=2)

	def confirm_additional_provider(self) -> None:
		"""
		Adds an additional provider and destroys the GUI element.
		:return: None
		"""
		temp_api_key = self.api_key_entry.get()
		temp_quota = self.quota_entry.get()
		temp_name = self.temp_name_label.cget("text")

		temp_image_provider = ImageProviderEntity(
			file_handler=self.application.file_handler,
			type_map_provider="Google Maps",
			api_key=temp_api_key,
			quota=temp_quota
		)

		self.user_entity.image_providers[temp_name] = temp_image_provider
		self.application.log_manager.write_log(self.user_entity)

		PreviewWindow(self.master, self.application, self.main_screen, self.coordinates)
		self.top.destroy()

	def confirm_download(self):
		self.top_label.configure(text="Are you sure you want to proceed?")
		self.top_label.grid(row=0, column=0, columnspan=3)

		for widget in self.temp_list:
			widget.grid_forget()

		counter = 2
		for provider in self.list_providers:

			self.provider_name = Label(self.top, text=str(provider[0]))
			self.provider_name.grid(row=counter, column=0)
			counter += 1

			cost_request_label_text = "Cost: " + str(provider[1])
			self.cost_request_label = Label(self.top, text=str(cost_request_label_text))
			self.cost_request_label.grid(row=counter, column=0)

			number_requests_label_text = "Images downloaded: " + str(provider[2])
			self.number_requests_label = Label(self.top, text=str(number_requests_label_text))
			self.number_requests_label.grid(row=counter, column=1)

			usage_left_label_text = "Usage left: " + str(provider[3])
			self.usage_left_label = Label(self.top, text=str(usage_left_label_text))
			self.usage_left_label.grid(row=counter, column=2)
			counter += 1

		self.nick_name_label = Label(self.top, text="Request name: \n(Optionl)")
		self.nick_name_label.grid(row=counter, column=0)

		self.name_entry = Entry(self.top)
		self.name_entry.grid(row=counter, column=1)
		counter += 1

		self.confirm_button = Button(
			self.top, text="Confirm", command=lambda: self.cleanup(self.coordinates), bg="white"
		)
		self.confirm_button.grid(row=counter, column=1)

	def cleanup(self, coordinates):
		"""
		Method called when the user clicks on the confirm button. Loads all the images associated
		with the locations and the updates the main screen
		:param locations: the locations to download
		:return: nothing (but updates the main screen with the downloaded image)
		"""
		name = self.name_entry.get()
		if name == "":
			name = None

		if len(coordinates) == 2:
			self.application.make_location_request(
				latitude=coordinates[0], longitude=coordinates[1], name=name
			)
		elif len(coordinates) == 4:
			self.application.make_area_request(
				bottom_latitude=coordinates[0],
				left_longitude=coordinates[1],
				top_latitude=coordinates[2],
				right_longitude=coordinates[3],
				name=name
			)
		else:
			raise ValueError("The number of coordinate values does not check out")

		self.top.destroy()
