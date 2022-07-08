"""
Module containing the TutorialWindow class
"""
from tkinter import Button, Label, Toplevel, W
from mesh_city.gui.widgets.button import Button as CButton
from mesh_city.gui.widgets.container import Container
from mesh_city.gui.widgets.widget_geometry import WidgetGeometry

from mesh_city.gui.search_window.search_window_start import SearchWindowStart
from mesh_city.util.screen_size_util import ScreenSizeUtil


class TutorialWindow:
	"""
	In case the user has not yet made a request, the tutorial window is loaded. Currently, it shows points the
	user to the window where they can make their first request
	"""

	def __init__(self, master, application, main_screen):
		"""
		The user is presented with all the options of the tutorial. Currently, it shows points the
		user to the window where they can make their first request
		:param master: the master tkinter object
		:param application: the global application context
		:param main_screen: the main screen
		"""
		self.main_screen = main_screen
		self.master = master
		self.value = ""
		self.application = application
		self.image_path = self.application.file_handler.folder_overview['image_path']
		self.top = Toplevel(master)

		self.top.config(padx=4)
		self.top.config(pady=4)

		self.top.attributes('-topmost', True)
		self.top.update()
		window_width, window_height, central_width, central_height = ScreenSizeUtil.get_curr_screen_geometry(680, 120)
		self.top.geometry("%dx%d+%d+%d" % (window_width, window_height, central_width, central_height))

		self.content = Container(WidgetGeometry(670, 110, 0, 0), self.top, background="white")
		layer_label_style = {"font": ("Eurostile LT Std", 18), "background": "white"}

		Label(
			self.content, text="It seems like this is the first time you use this application.", **layer_label_style,
		).place(width=660, height=40, x=0, y=0)

		CButton(
			WidgetGeometry(450, 50, 110, 50),
			"Click here to make your first request",
			lambda _: self.cleanup(),
			self.content,
		)


		# self.top_label = Label(
		# 	self.top, text="It seems like this is the first time you use this application."
		# )
		# self.top_label.grid(row=0)
		#
		# self.search_button = Button(
		# 	self.top, text="Click here to make your first request", command=self.cleanup, bg="white"
		# )
		# self.search_button.grid(row=1)

	def cleanup(self):
		"""
		Currently opens the search window where they can make their first request
		:return: nothing (the search window is opened)
		"""
		temp_window = SearchWindowStart(self.master, self.application, self.main_screen)
		self.top.destroy()
		self.main_screen.master.wait_window(temp_window.top)
