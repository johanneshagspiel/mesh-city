"""
A module containing the preview window
"""
from tkinter import Button, Label, Toplevel

from mesh_city.imagery_provider.top_down_provider_factory import TopDownProviderFactory
from mesh_city.util.price_table_util import PriceTableUtil, QuotaException


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
		top_down_factory = TopDownProviderFactory()
		self.application.request_maker.top_down_provider = top_down_factory.get_top_down_provider(
			image_provider_entity
		)
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
				bottom_lat=self.coordinates[0], left_long=self.coordinates[1],
				top_lat=self.coordinates[2], right_long=self.coordinates[3])
		else:
			raise ValueError("The number of coordinate values does not check out")
		print(locations)
		number_requests = self.application.request_maker.count_uncached_tiles(locations)

		for widget in self.temp_list:
			widget.grid_forget()

		self.top_label.configure(text="Are you sure you want to proceed?")

		number_requests_label_text = "Images to download: " + str(number_requests)
		self.number_requests_label = Label(self.top, text=str(number_requests_label_text))
		self.number_requests_label.grid(row=1, column=0)
		try:
			temp_cost = PriceTableUtil.calculate_action_price(
				image_provider_entity.type,
				"static_map",
				image_provider_entity.usage["static_map"],
				number_requests,
				image_provider_entity.quota
			)
		except ValueError:
			# should be integrated into the GUI
			print("The value is not defined")
		except QuotaException:
			# should be integrated into the GUI
			print("This would exceed the quota")
		else:
			cost_request_label_text = "Cost: " + str(temp_cost)
			self.cost_request_label = Label(self.top, text=str(cost_request_label_text))
			self.cost_request_label.grid(row=2, column=0)

			usage_left_label_text = "Usage left: " + str(image_provider_entity.quota - temp_cost)
			self.usage_left_label = Label(self.top, text=str(usage_left_label_text))
			self.usage_left_label.grid(row=3, column=0)

			self.confirm_button = Button(
				self.top, text="Confirm", command=lambda: self.cleanup(self.coordinates)
			)
			self.confirm_button.grid(row=4)

	def cleanup(self, coordinates):
		"""
		Method called when the user clicks on the confirm button. Loads all the images associated
		with the locations and the updates the main screen
		:param locations: the locations to download
		:return: nothing (but updates the main screen with the downloaded image)
		"""
		# this is a location request
		if len(coordinates) == 2:
			self.application.make_location_request(
				latitude=coordinates[0], longitude=coordinates[1]
			)
		elif len(coordinates) == 4:
			self.application.make_area_request(
				bottom_latitude=coordinates[0],
				left_longitude=coordinates[1],
				top_latitude=coordinates[2],
				right_longitude=coordinates[3]
			)
		else:
			raise ValueError("The number of coordinate values does not check out")

		self.top.destroy()
