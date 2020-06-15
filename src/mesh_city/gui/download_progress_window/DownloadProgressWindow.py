from tkinter import Label, Toplevel
from threading import Timer

class DownloadProgressWindow:

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

		self.images_to_download_label = Label(self.top, text="sdf")
		self.images_to_download_label.grid(row=0, column=0)

		self.time_remaining_label = Label(self.top, text="sdf")
		self.time_remaining_label.grid(row=1, column=0)

		print("hi")
		self.update_gui()

		t = Timer(1, self.update_gui)
		t.start()

	def update_gui(self):
		images_to_download = "Progress: " + str(self.application.request_observer.current_image) + " out of " + str(self.application.request_observer.total_images) + " images"
		self.images_to_download_label["text"] = images_to_download

		time_remaining = "Time remaining for download: " + str(self.application.request_observer.estimated_time_to_finish)
		self.time_remaining_label["text"] = time_remaining

		print("hi2")
