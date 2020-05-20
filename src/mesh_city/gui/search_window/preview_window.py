from tkinter import Button, Entry, Label, Toplevel

class PreviewWindow:

	def __init__(self, master, application, main_screen, coordinates):
		self.main_screen = main_screen
		self.master = master
		self.value = coordinates
		self.application = application
		top = self.top = Toplevel(master)

		self.top_label = Label(top, text="Which image provider do you want to use?")
		self.top_label.grid(row=0, column=3)

		number_images = self.application.request_manager.calculate_locations(coordinates=coordinates, zoom=20)
		self.nuber_requests = Label(top, text=str(number_images))
		self.nuber_requests.grid(row=1, column=1)

	def cleanup(self):
		"""
		Makes the area-type request and cleans up after itself by tearing down the GUI and
		effectively returning control to the main screen.
		"""
		self.value = [
			float(self.min_lat_entry.get()),
			float(self.min_long_entry.get()),
			float(self.max_lat_entry.get()),
			float(self.max_long_entry.get()),
		]

		self.application.request_manager.make_request_for_block(self.value)

		# self.application.file_handler.folder_overview["active_tile_path"][0] = \
		# 	Path.joinpath(self.application.file_handler.folder_overview["image_path"][0], name_directory, "0_tile_0_0")
		#
		# self.application.file_handler.folder_overview["active_image_path"][0] = \
		# 	Path.joinpath(self.application.file_handler.folder_overview["image_path"][0], name_directory, "0_tile_0_0")
		#
		# self.application.file_handler.folder_overview["active_request_path"][0] = \
		# 	self.application.file_handler.folder_overview["active_tile_path"][0].parents[0]
		#
		# self.main_screen.currently_active_tile = self.application.request_manager.active_tile_path
		# self.main_screen.currently_active_request = Path(self.main_screen.currently_active_tile
		# 												).parents[0]
		self.main_screen.update_image()
		self.top.destroy()
