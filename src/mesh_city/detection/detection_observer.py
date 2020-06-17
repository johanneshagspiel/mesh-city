"""
The module containing the detection observer
"""
from tkinter import Label, Toplevel


class DetectionObserver:
	"""
	This class both observers request maker and acts as a progress bar indicating how far the download has progresed
	"""

	def __init__(self, master):
		"""
		The initialization method
		:param master: the master tkinter object
		"""
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

		self.top_label = Label(self.top, text="")
		self.top_label.grid(row=0, column=0)

		self.tiles_to_detect = Label(self.top, text="")
		self.tiles_to_detect.grid(row=1, column=0)

		self.time_remaining_label = Label(self.top, text="")
		self.time_remaining_label.grid(row=2, column=0)

	def update(self, detection_pipeline):
		"""
		Method called by the observee to indicate that a state has changed. It means that another tile has been detected
		:param detection_pipeline:
		:return:
		"""
		self.total_tiles = detection_pipeline.state["total_tiles"]
		self.current_tile = detection_pipeline.state["current_tile"]
		self.current_time_detection = detection_pipeline.state["current_time_detection"]
		self.detection_type = detection_pipeline.state["detection_type"]

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
