"""
The module containing the request observer
"""
from tkinter import Label, Toplevel


class RequestObserver:
	"""
	This class both observers request maker and acts as a progress bar indicating how far the download has progresed
	"""

	def __init__(self, master):
		"""
		The initialization method
		:param master: the master tkinter object
		"""
		self.total_images = 0
		self.current_image = 0
		self.missing_images = 0
		self.current_time_download = 0
		self.duration_so_far = 0
		self.estimated_time_to_finish = 0

		self.master = master
		self.top = Toplevel(master)

		self.images_to_download_label = Label(self.top, text="")
		self.images_to_download_label.grid(row=0, column=0)

		self.time_remaining_label = Label(self.top, text="")
		self.time_remaining_label.grid(row=1, column=0)

	def update(self, request_maker):
		"""
		Method called by the observee to indicate that a state has changed. It means that another image has been downloaded
		:param request_maker:
		:return:
		"""
		self.total_images = request_maker.state["total_images"]
		self.current_image = request_maker.state["current_image"]
		self.current_time_download = request_maker.state["current_time_download"]
		self.update_estimated_time_to_finish()
		self.update_gui()

	def update_estimated_time_to_finish(self):
		"""
		Helper method to calculate the average time needed for the remaining downloads
		:return:
		"""
		self.missing_images = self.total_images - self.current_image
		self.duration_so_far += self.current_time_download
		self.estimated_time_to_finish = self.missing_images * (
			self.duration_so_far / self.current_image
		)

	def update_gui(self):
		"""
		When the observer is notified of a change, the gui needs to be udpated to reflect the change
		:return:
		"""
		images_to_download = "Progress: " + str(self.current_image) + " out of " + str(
			self.total_images
		) + " images downloaded"
		self.images_to_download_label["text"] = images_to_download

		time_remaining = "Time remaining: " + str(
			round(self.estimated_time_to_finish, 2)
		) + " seconds"
		self.time_remaining_label["text"] = time_remaining

		self.images_to_download_label.update()
		self.time_remaining_label.update()

	def destroy(self):
		"""
		Method called when the observee detaches the observer - destroys the gui element
		:return:
		"""
		self.top.destroy()
