"""
The module containing the detection observer
"""
from tkinter import Label, Toplevel

from mesh_city.gui.widgets.container import Container
from mesh_city.gui.widgets.widget_geometry import WidgetGeometry
from mesh_city.util.observable import Observable
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
		self.previous_detection_type = ""
		self.duration_so_far = 0

		self.master = master
		self.top = Toplevel(master)

		self.top.grab_set()

		self.top.geometry("%dx%d+%d+%d" % (560, 145, 0, 0))
		layer_label_style = {
			"font": ("Eurostile LT Std", 18), "background": "white", "anchor": "center"
		}

		self.content = Container(WidgetGeometry(550, 135, 5, 5), self.top, background="white")

		self.top_label = Label(
			self.content, text="Initializing the algorithms", **layer_label_style
		)
		self.top_label.place(width=550, height=40, x=10, y=0)

		self.time_remaining_label = Label(self.content, text="", **layer_label_style)

		self.tiles_to_detect = Label(self.content, text="", **layer_label_style)

		self.top_label.update()

	def update(self, observable: Observable):
		"""
		Method called by the observee to indicate that a state has changed. It means that another tile has been detected
		:param observable: The observable this class has subscribed to
		:return:
		"""
		total_tiles = observable.observable_state["total_tiles"]
		current_tile = observable.observable_state["current_tile"]
		time_of_action = observable.observable_state["current_time_detection"]
		detection_type = observable.observable_state["detection_type"]

		if detection_type != self.previous_detection_type:
			self.duration_so_far = 0
		self.duration_so_far += time_of_action
		finish_time = self.compute_estimated_finish_time(
			number_of_actions=total_tiles, number_of_actions_done=current_tile
		)
		self.update_gui(
			detection_type=detection_type,
			current_tile=current_tile,
			total_tiles=total_tiles,
			finish_time_estimate=finish_time
		)
		self.previous_detection_type = detection_type

	def compute_estimated_finish_time(
		self, number_of_actions: int, number_of_actions_done: int
	) -> float:
		"""
		Computes an estimate for the finish time.
		:param number_of_actions: The number of actions that have to be completed in total
		:param number_of_actions_done: The number of actions that have been completed already
		:return: An estimate of the finish time of the remaining actions
		"""
		return (number_of_actions -
			number_of_actions_done) * (self.duration_so_far / number_of_actions_done)

	def update_gui(
		self, detection_type: str, current_tile: int, total_tiles: int, finish_time_estimate: float
	) -> None:
		"""
		Updates the GUI based on a set of numbers derived from an observed DetectionPipeline
		:param detection_type: A string representation of what is being detected by the pipeline.
		:param current_tile: Which tile out of the total number of tile is being processed
		:param total_tiles: The total number of tiles that have to be processed by the pipeline.
		:param finish_time_estimate: An estimate of the finish time
		:return: None
		"""

		self.tiles_to_detect.place(width=550, height=40, x=10, y=50)
		self.time_remaining_label.place(width=550, height=40, x=10, y=100)

		top_label_text = "Currently detecting: " + detection_type
		self.top_label["text"] = top_label_text

		images_to_download = "Progress: " + str(current_tile) + " out of " + str(
			total_tiles
		) + " tiles detected"
		self.tiles_to_detect["text"] = images_to_download

		time_remaining = "Time remaining: " + str(round(finish_time_estimate, 2)) + " seconds"
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
