"""
A module containing the preview window
"""
from tkinter import Button, END, Label, Toplevel, Entry

from mesh_city.gui.error_windows.additional_provider_error import AdditionalProviderError
from mesh_city.util.price_table_util import PriceTableUtil


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
		top = self.top = Toplevel(master)

		self.top.config(padx=4)
		self.top.config(pady=4)

		self.top_label = Label(top, text="Which image provider do you want to use?")
		self.top_label.grid(row=0, columnspan=2)

		self.count = 1
		self.temp_list = []
		self.temp_list_size = -1

		self.provider_number = 0

		for key, value in self.application.user_entity.image_providers.items():
			self.provider_number += 1
			self.temp_list.append(
				Button(
				self.top, text=key, command=lambda value=value: self.check_usage(key, value), bg="white"
				)
			)
			self.temp_list_size += 1
			self.temp_list[self.temp_list_size].grid(row=self.count, column=0)

			temp_text = "Usage left: " + str(value.quota - value.usage["total"])
			self.temp_list.append(Label(self.top, text=temp_text))
			self.temp_list_size += 1
			self.temp_list[self.temp_list_size].grid(row=self.count, column=1)
			self.count += 1

		self.additional_provider_button = Button(
			self.top, text="Add new image provider", command=self.add_another_provider, bg="white")
		self.additional_provider_button.grid(row=self.count, columnspan=2)

	def add_another_provider(self):
		self.provider_number += 1
		self.count += 1

		temp_name = str("Google Maps ") + str(self.provider_number)
		self.provider_number += 1
		self.temp_name_label = Label(self.top, text=temp_name)
		self.temp_name_label.grid(row=self.count, column=0)
		self.count += 1

		self.api_key = Label(self.top, text="API Key")
		self.api_key.grid(row=self.count, column=0)

		self.api_key_entry = Entry(self.top)
		self.api_key_entry.grid(row=self.count, column=1, columnspan=2)
		self.count += 1

		self.quota = Label(self.top, text="Monthly Quota")
		self.quota.grid(row=self.count, column=0)

		self.quota_entry = Entry(self.top)
		self.quota_entry.grid(row=self.count, column=1, columnspan=2)
		self.count += 1

		self.confirm_button = Button(self.top, text="Confirm", command=None)
		self.confirm_button.grid(row=self.count, column=1)
		self.additional_provider_button.grid_forget()

	def check_usage(self, image_provider_entity_name, image_provider_entity):
		"""
		Method to check how much this request would cost
		:param image_provider_entity: the image provider entity used for the request
		:return: nothing (updates the gui to show how much the request would cost)
		"""
		self.application.request_manager.image_provider = image_provider_entity
		self.application.request_manager.top_down_provider = image_provider_entity.top_down_provider
		self.locations = self.application.request_manager.calculate_locations(
			coordinates=self.coordinates
		)
		self.locations = self.application.request_manager.check_coordinates(self.locations)
		number_requests = self.locations.pop(0)

		for widget in self.temp_list:
			widget.grid_forget()

		self.top_label.configure(text="Are you sure you want to proceed?")

		number_requests_label_text = "Images to download: " + str(number_requests)
		self.number_requests_label = Label(self.top, text=str(number_requests_label_text))
		self.number_requests_label.grid(row=1, column=0)
		temp_cost = PriceTableUtil.calculate_action_price(
			image_provider_entity.type,
			"static_map",
			number_requests,
			image_provider_entity.quota)

		if temp_cost[0] != -1:
			cost_request_label_text = "Cost: " + str(temp_cost)
			self.cost_request_label = Label(self.top, text=str(cost_request_label_text))
			self.cost_request_label.grid(row=2, column=0)

			usage_left_label_text = "Usage left: " + str(image_provider_entity.quota - temp_cost)
			self.usage_left_label = Label(self.top, text=str(usage_left_label_text))
			self.usage_left_label.grid(row=3, column=0)

			self.confirm_button = Button(
				self.top, text="Confirm", command=lambda: self.cleanup(self.locations), bg="white"
			)
			self.confirm_button.grid(row=4)
		else:
			providers_selected = [image_provider_entity_name]
			images_remaining = temp_cost[2]
			enough = False

			for key, value in self.application.user_entity.image_providers.items():
				if key not in providers_selected:
					temp_cost_2 = PriceTableUtil.calculate_action_price(
						value.type,
						"static_map",
						images_remaining,
						value.quota)
					providers_selected.append(key)
					if temp_cost_2[0] != -1:
						enough = True
						pass

			if enough:
				return None
			else:
				AdditionalProviderError(self.master, self.application, images_remaining, providers_selected)
				self.top.destroy()


	def cleanup(self, locations):
		"""
		Method called when the user clicks on the confirm button. Loads all the images associated
		with the locations and the updates the main screen
		:param locations: the locations to download
		:return: nothing (but updates the main screen with the downloaded image)
		"""

		self.application.request_manager.make_request_for_block(locations)
		self.main_screen.update_image()

		self.main_screen.information_general.configure(state='normal')
		self.main_screen.information_general.delete('1.0', END)
		self.main_screen.information_general.insert(END, "General")
		self.main_screen.information_general.configure(state='disabled')

		self.top.destroy()
