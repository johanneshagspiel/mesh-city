"""
A module containing the detection screen
"""
from tkinter import Button, Checkbutton, IntVar, Label, Toplevel


class DetectionWindow:
	"""
	The detection screen where one can select what to detect i.e. trees. The main_screen then will be
	updated automatically
	"""
	DETECTION_OPTIONS = {"Trees"}

	def __init__(self, master, application):
		"""
		The initialization method
		:param master: the master tkinter object
		:param application: the global application context
		:param main_screen: the main_screen of the application
		"""
		self.master = master
		self.application = application
		self.top = Toplevel(master)

		# TODO update with new detection options
		self.top_label = Label(self.top, text="What do you want to detect?")
		self.top_label.grid(row=0)

		print(self.application.file_handler.folder_overview["active_request_path"])
		temp_path = next(
			self.application.file_handler.folder_overview["active_request_path"].
			glob('building_instructions_request_*')
		)
		self.building_instructions = self.application.log_manager.read_log(
			temp_path, "building_instructions_request"
		)

		to_detect = self.get_undetected_features(self.building_instructions)

		if len(to_detect) == 0:
			self.top_label["text"] = "You have already detected everything"

		else:
			self.check_box_list = []
			self.checkbox_int_variables = []
			temp_counter = 0

			for counter, element in enumerate(to_detect, 1):
				self.checkbox_int_variables.append(IntVar())
				self.check_box_list.append(
					Checkbutton(
					self.top, text=element, variable=self.checkbox_int_variables[counter - 1]
					)
				)
				self.check_box_list[counter - 1].grid(row=counter)
				temp_counter = counter
			self.confirm_button = Button(
				self.top, text="Confirm", command=lambda: self.cleanup(self.building_instructions)
			)
			self.confirm_button.grid(row=temp_counter + 1)

	def get_undetected_features(self, building_instructions):
		temp_list_detected_layers = []
		for key in building_instructions.instructions.keys():
			# TODO change if we ever add another image provider
			if key != "Google Maps":
				temp_list_detected_layers.append(key)
		to_detect = list(
			DetectionWindow.DETECTION_OPTIONS.symmetric_difference(temp_list_detected_layers)
		)
		return to_detect

	def cleanup(self, building_instructions):
		"""
		Method called on button press: runs the appropriate detection algorithm, updates the image
		on the main_screen and then closes itself
		:return:
		"""
		selected_detections = []
		for (index, element) in enumerate(self.checkbox_int_variables):
			if element.get() == 1:
				selected_detections.append(self.check_box_list[index].cget("text"))
		if len(selected_detections) > 0:
			self.application.run_detection(
				building_instructions=building_instructions, to_detect=selected_detections
			)
		self.top.destroy()
