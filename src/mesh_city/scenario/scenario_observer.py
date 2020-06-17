"""
The module containing the scenario observer
"""
from tkinter import Label, Toplevel

from mesh_city.util.observer import Observer


class ScenarioObserver(Observer):
	"""
	This class both observers request maker and acts as a progress bar indicating how far the download has progresed
	"""

	def __init__(self, master):
		"""
		The initialization method
		:param master: the master tkinter object
		"""
		super().__init__()
		self.total_frames = 0
		self.current_frame = 0
		self.scenario_type = ""

		self.missing_frames = 0
		self.previous_scenario_type = ""

		self.master = master
		self.top = Toplevel(master)

		self.top_label = Label(self.top, text="Warming up the algorithms")
		self.top_label.grid(row=0, column=0)
		self.time_remaining_label = Label(self.top, text="")

		self.frames_to_detect = Label(self.top, text="")

		self.top_label.update()

	def update(self, observee):
		"""
		Method called by the observee to indicate that a state has changed. It means that another tile has been detected
		:param scenario_pipeline: the scenario pipeline to observer
		:return:
		"""
		self.total_frames = observee.state["total_frames"]
		self.current_frame = observee.state["current_frame"]
		self.scenario_type = observee.state["scenario_type"]

		if self.scenario_type != self.previous_scenario_type:
			self.missing_frames = 0
			self.duration_so_far = 0
			self.estimated_time_to_finish = 0

		self.update_gui()
		self.previous_scenario_type = self.scenario_type

	def update_gui(self):
		"""
		Once the observer has been notified of a change, the gui needs to be updated
		:return:
		"""

		self.frames_to_detect.grid(row=1, column=0)

		top_label_text = "Current scenario: " + self.scenario_type
		self.top_label["text"] = top_label_text

		frames_to_detect_text = "Progress: " + str(self.current_frame) + " out of " + str(
			self.total_frames
		) + " Frames created"
		self.frames_to_detect["text"] = frames_to_detect_text

		self.top_label.update()
		self.frames_to_detect.update()

	def update_combination(self):
		"""
		How to update the gui in the case images are combined
		:return:
		"""
		self.top_label["text"] = "Combining all the frames"
		self.top_label.update()
		self.frames_to_detect["text"] = "One moment please"
		self.frames_to_detect.update()

	def destroy(self):
		"""
		Method called when the observee detaches the observer - destroys the gui element
		:return:
		"""
		self.top.destroy()
