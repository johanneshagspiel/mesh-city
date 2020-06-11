"""
A module containing the detection screen
"""
from tkinter import Button, Checkbutton, IntVar, Label, Toplevel

from mesh_city.detection.pipeline import DetectionType
from mesh_city.request.trees_layer import TreesLayer


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

		to_detect = []
		if not self.application.current_request.has_layer_of_type(TreesLayer):
			to_detect.append(DetectionType.Trees)

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
			self.confirm_button = Button(self.top, text="Confirm", command=lambda: self.cleanup())
			self.confirm_button.grid(row=temp_counter + 1)

	def cleanup(self):
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
				request=self.application.current_request, to_detect=selected_detections
			)
		self.top.destroy()
