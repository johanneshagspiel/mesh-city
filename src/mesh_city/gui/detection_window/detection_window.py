"""
A module containing the detection screen
"""
from tkinter import Button, Checkbutton, IntVar, Label, Toplevel

from mesh_city.detection.pipeline import Pipeline


class DetectionWindow:
	"""
	The detection screen where one can select what to detect i.e. trees. The main_screen then will be
	updated automatically
	"""

	def __init__(self, master, application, main_screen):
		"""
		The initialization method
		:param master: the master tkinter object
		:param application: the global application context
		:param main_screen: the main_screen of the application
		"""
		self.main_screen = main_screen
		self.master = master
		self.value = ""
		self.application = application
		self.top = Toplevel(master)

		# TODO update with new detection options
		self.list_detection_options = ["Trees", "Buildings"]

		self.top_label = Label(self.top, text="What do you want to detect?")
		self.top_label.grid(row=0)

		temp_path = next(
			self.application.file_handler.folder_overview["active_request_path"].
			glob('building_instructions_request_*')
		)
		self.building_instructions = self.application.log_manager.read_log(
			temp_path, "building_instructions_request"
		)

		temp_list_detected_layers = []
		for key in self.building_instructions.instructions.keys():
			# TODO change if we ever add another image provider
			if key != "Google Maps":
				temp_list_detected_layers.append(key)

		to_detect = list(
			set(self.list_detection_options).symmetric_difference(temp_list_detected_layers)
		)

		if len(to_detect) == 0:
			self.top_label["text"] = "You have already detected everything"

		else:
			self.check_box_list = []
			self.temp_int_var_list = []
			temp_counter = 0

			for counter, element in enumerate(to_detect, 1):
				self.temp_int_var_list.append(IntVar())
				self.check_box_list.append(
					Checkbutton(self.top, text=element, variable=self.temp_int_var_list[counter - 1])
				)
				self.check_box_list[counter - 1].grid(row=counter)
				temp_counter = counter

			self.confirm_button = Button(
				self.top, text="Confirm", command=lambda: self.cleanup(self.building_instructions)
			)
			self.confirm_button.grid(row=temp_counter + 1)

	# pylint: disable= W0613
	def cleanup(self, building_instructions):
		"""
		Method called on button press: runs the appropriate detection algorithm, updates the image
		on the main_screen and then closes itself
		:return:
		"""

		to_detect = []
		temp_counter = 0
		temp_sum = 0

		for element in self.temp_int_var_list:
			if element.get() == 1:
				to_detect.append(self.check_box_list[temp_counter].cget("text"))
				temp_sum += 1
			temp_counter += 1

		if temp_sum == 0:
			self.top.destroy()

		else:
			Pipeline(self.application, self.main_screen, to_detect,
				self.building_instructions).push_forward()
			self.main_screen.active_layers = to_detect
			self.main_screen.update_image()
			self.main_screen.update_text()
			self.top.destroy()
