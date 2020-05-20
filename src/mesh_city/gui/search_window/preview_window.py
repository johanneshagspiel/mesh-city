from tkinter import Button, Label, Toplevel
from mesh_city.util.price_table_util import PriceTableUtil

class PreviewWindow:

	def __init__(self, master, application, main_screen, coordinates):
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

		for key,value in self.application.user_entity.image_providers.items():
			self.temp_list.append(Button(self.top, text=key, command=lambda value=value: self.check_usage(value)))
			self.temp_list_size += 1
			self.temp_list[self.temp_list_size].grid(row=self.count, column=0)

			temp_text = "Usage left: " + str(value.quota - value.usage["total"])
			self.temp_list.append(Label(self.top, text=temp_text))
			self.temp_list_size += 1
			self.temp_list[self.temp_list_size].grid(row=self.count, column=1)
			self.count += 1

	def check_usage(self, value):
		self.application.request_manager.map_entity = value.map_entity
		self.locations = self.application.request_manager.calculate_locations(coordinates=self.coordinates)
		number_requests = len(self.locations)

		for widget in self.temp_list:
			widget.grid_forget()

		self.top_label.configure(text="Are you sure you want to proceed?")

		number_requests_label_text = "Images to download: " + str(number_requests)
		self.number_requests_label = Label(self.top, text=str(number_requests_label_text))
		self.number_requests_label.grid(row=1, column=0)

		action = [("static_map", number_requests)]
		temp_cost = PriceTableUtil(image_provider_entity=value, action=action).calculate_action_price()

		if temp_cost[0] == "NAN":
			print("NAN")
			print(temp_cost[1])
			print(temp_cost[2])
			return None

		if temp_cost[0] == "Quota":
			print("Quota")
			print(temp_cost[1])
			print(temp_cost[2])
			return None

		cost_request_label_text = "Cost: " + str(temp_cost[0])
		self.cost_request_label = Label(self.top, text=str(cost_request_label_text))
		self.cost_request_label.grid(row=2, column=0)

		usage_left_label_text = "Usage left: " + str(value.quota - temp_cost[0])
		self.usage_left_label = Label(self.top, text=str(usage_left_label_text))
		self.usage_left_label.grid(row=3, column=0)

		self.confirm_button = Button(self.top, text="Confirm", command=lambda : self.cleanup(self.locations))
		self.confirm_button.grid(row=4)

	def cleanup(self, locations):

		self.application.request_manager.make_request_for_block(locations)
		self.main_screen.update_image()
		self.top.destroy()
