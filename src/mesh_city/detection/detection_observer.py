"""
The module containing the detection observer
"""
from tkinter import Label, Toplevel

from mesh_city.util.observer import Observer


class DetectionObserver(Observer):
	"""
	This class both observers request maker and acts as a progress bar indicating how far the download has progresed
	"""

	def __init__(self, master):
		"""
		The initialization method
		:param master: the master tkinter object
		"""
		super().__init__()

		self.total_tiles = 0
		self.current_tile = 0
		self.current_time_detection = 0
		self.detection_type = ""

		self.missing_tiles = 0
		self.duration_so_far = 0
		self.estimated_time_to_finish = 0
		self.previous_detection_type = ""

		self.master = master
		self.top = Toplevel(master)

		self.top_label = Label(self.top, text="Warming up the algorithms")
		self.top_label.grid(row=0, column=0)
		self.time_remaining_label = Label(self.top, text="")

		self.tiles_to_detect = Label(self.top, text="")

		self.top_label.update()

	def update(self, observee):
		"""
		Method called by the observee to indicate that a state has changed. It means that another tile has been detected
		:param detection_pipeline: the detection pipeline to observer
		:return:
		"""
		self.total_tiles = observee.state["total_tiles"]
		self.current_tile = observee.state["current_tile"]
		self.current_time_detection = observee.state["current_time_detection"]
		self.detection_type = observee.state["detection_type"]

		if self.detection_type != self.previous_detection_type:
			self.missing_tiles = 0
			self.duration_so_far = 0
			self.estimated_time_to_finish = 0

		self.update_estimated_time_to_finish()
		self.update_gui()
		self.previous_detection_type = self.detection_type

	def update_estimated_time_to_finish(self):
		"""
		Helper method to calculate the average time needed for the remaining detections
		:return:
		"""
		self.missing_tiles = self.total_tiles - self.current_tile
		self.duration_so_far += self.current_time_detection
		self.estimated_time_to_finish = self.missing_tiles * (
			self.duration_so_far / self.current_tile
		)

	def update_gui(self):
		"""
		Once the observer has been notified of a change, the gui needs to be updated
		:return:
		"""

		self.tiles_to_detect.grid(row=1, column=0)
		self.time_remaining_label.grid(row=2, column=0)

		top_label_text = "Currently detecting: " + self.detection_type
		self.top_label["text"] = top_label_text

		images_to_download = "Progress: " + str(self.current_tile) + " out of " + str(
			self.total_tiles
		) + " tiles detected"
		self.tiles_to_detect["text"] = images_to_download

		time_remaining = "Time remaining: " + str(
			round(self.estimated_time_to_finish, 2)
		) + " seconds"
		self.time_remaining_label["text"] = time_remaining

		self.top_label.update()
		self.tiles_to_detect.update()
		self.time_remaining_label.update()

	def destroy(self):
		"""
		Method called when the observee detaches the observer - destroys the gui element
		:return:
		"""
		self.top.destroy()
