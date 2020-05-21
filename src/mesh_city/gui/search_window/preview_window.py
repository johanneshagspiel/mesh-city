"""
A module containing the preview window
"""
from tkinter import Button, Label, Toplevel

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
		:param coordinates: the coordinates of the request
		"""
		self.main_screen = main_screen
		self.master = master
		self.coordinates = coordinates
		self.application = application
		top = self.top = Toplevel(master)

		self.top_label = Label(top, text="Which image provider do you want to use?")
		self.top_label.grid(row=0, columnspan=2)

		self.count = 1
		self.temp_list = []
		self.temp_list_size = -1

		for key, value in self.application.user_entity.image_providers.items():
			self.temp_list.append(
				Button(self.top, text=key, command=lambda value=value: self.check_usage(value))
			)
			self.temp_list_size += 1
			self.temp_list[self.temp_list_size].grid(row=self.count, column=0)

			temp_text = "Usage left: " + str(value.quota - value.usage["total"])
			self.temp_list.append(Label(self.top, text=temp_text))
			self.temp_list_size += 1
			self.temp_list[self.temp_list_size].grid(row=self.count, column=1)
			self.count += 1

	def check_usage(self, image_provider_entity):
		"""
		Method to check how much this request would cost
		:param image_provider_entity: the image provider entity used for the request
		:return: nothing (updates the gui to show how much the request would cost)
		"""
		self.application.request_manager.map_entity = image_provider_entity.map_entity
		self.locations = self.application.request_manager.calculate_locations(
			coordinates=self.coordinates
		)
		number_requests = len(self.locations)

		for widget in self.temp_list:
			widget.grid_forget()

		self.top_label.configure(text="Are you sure you want to proceed?")

		number_requests_label_text = "Images to download: " + str(number_requests)
		self.number_requests_label = Label(self.top, text=str(number_requests_label_text))
		self.number_requests_label.grid(row=1, column=0)

		("static_map", number_requests)
		print()
		temp_cost = PriceTableUtil.calculate_action_price(
			image_provider_entity.type,
			"static_map",
			image_provider_entity.usage["static_map"],
			number_requests,
			image_provider_entity.quota
		)
		cost_request_label_text = "Cost: " + str(temp_cost)
		self.cost_request_label = Label(self.top, text=str(cost_request_label_text))
		self.cost_request_label.grid(row=2, column=0)

		usage_left_label_text = "Usage left: " + str(image_provider_entity.quota - temp_cost)
		self.usage_left_label = Label(self.top, text=str(usage_left_label_text))
		self.usage_left_label.grid(row=3, column=0)

		self.confirm_button = Button(
			self.top, text="Confirm", command=lambda: self.cleanup(self.locations)
		)
		self.confirm_button.grid(row=4)

	def cleanup(self, locations):
		"""
		Method called when the user clicks on the confirm button. Loads all the images associated
		with the locations and the updates the main screen
		:param locations: the locations to download
		:return: nothing (but updates the main screen with the downloaded image)
		"""

		self.application.request_manager.make_request_for_block(locations)
		self.main_screen.update_image()
		self.top.destroy()
