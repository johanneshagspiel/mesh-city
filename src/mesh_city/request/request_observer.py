"""
The module containing the request observer
"""
from tkinter import Label, Toplevel

from mesh_city.gui.widgets.container import Container
from mesh_city.gui.widgets.widget_geometry import WidgetGeometry
from mesh_city.util.observer import Observer


class RequestObserver(Observer):
	"""
	This class both observers request maker and acts as a progress bar indicating how far the download has progresed
	"""

	def __init__(self, master):
		"""
		The initialization method
		:param master: the master tkinter object
		"""
		super().__init__()

		self.total_images = 0
		self.current_image = 0
		self.missing_images = 0
		self.current_time_download = 0
		self.duration_so_far = 0
		self.estimated_time_to_finish = 0

		self.master = master
		self.top = Toplevel(master)

		self.top.geometry("%dx%d+%d+%d" % (560, 145, 0, 0))
		layer_label_style = {
			"font": ("Eurostile LT Std", 18), "background": "white", "anchor": "center"
		}

		self.content = Container(WidgetGeometry(550, 135, 5, 5), self.top, background="white")

		self.top_label = Label(self.content, text="Initializing the algorithms", **layer_label_style)
		self.top_label.place(width=550, height=40, x=10, y=0)

		self.images_to_download_label = Label(self.content, text="", **layer_label_style)
		self.images_to_download_label.place(width=550, height=40, x=10, y=50)

		self.time_remaining_label = Label(self.content, text="", **layer_label_style)
		self.time_remaining_label.place(width=550, height=40, x=10, y=100)

	def update(self, observable):
		"""
		Method called by the observable to indicate that a state has changed. It means that another image has been downloaded
		:param request_maker:
		:return:
		"""
		self.total_images = observable.observable_state["total_images"]
		self.current_image = observable.observable_state["current_image"]
		self.current_time_download = observable.observable_state["current_time_download"]
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
