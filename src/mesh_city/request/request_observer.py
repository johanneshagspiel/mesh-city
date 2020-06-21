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

		self.duration_so_far = 0

		self.master = master
		self.top = Toplevel(master)

		self.top.geometry("%dx%d+%d+%d" % (560, 145, 0, 0))
		layer_label_style = {
			"font": ("Eurostile LT Std", 18), "background": "white", "anchor": "center"
		}

		self.content = Container(WidgetGeometry(550, 135, 5, 5), self.top, background="white")

		self.top_label = Label(self.content, text="Initializing the algorithms",
		                       **layer_label_style)
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
		total_tiles = observable.observable_state["total_images"]
		current_tile = observable.observable_state["current_image"]
		time_of_action = observable.observable_state["current_time_download"]
		self.duration_so_far += time_of_action
		finish_time = self.compute_estimated_finish_time(number_of_actions=total_tiles,
		                                                 number_of_actions_done=current_tile)
		self.update_gui(current_tile=current_tile,
		                total_tiles=total_tiles, finish_time_estimate=finish_time)

	def compute_estimated_finish_time(self, number_of_actions: int,
	                                  number_of_actions_done: int) -> float:
		"""
		Computes an estimate for the finish time.
		:param number_of_actions: The number of actions that have to be completed in total
		:param number_of_actions_done: The number of actions that have been completed already
		:return: An estimate of the finish time of the remaining actions
		"""
		return (number_of_actions - number_of_actions_done) * (
			self.duration_so_far / number_of_actions_done
		)

	def update_gui(self, current_tile: int, total_tiles: int,
	               finish_time_estimate: float) -> None:
		"""
		Updates the GUI based on a set of numbers derived from an observed RequestMaker
		:param current_tile:
		:param total_tiles:
		:param finish_time_estimate:
		:return:
		"""
		images_to_download = "Progress: " + str(current_tile) + " out of " + str(
			total_tiles
		) + " images downloaded"
		self.images_to_download_label["text"] = images_to_download

		time_remaining = "Time remaining: " + str(
			round(finish_time_estimate, 2)
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
