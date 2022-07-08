"""
See :class:`.SearchWindowStart`
"""

from tkinter import Label, Toplevel, W

from mesh_city.gui.search_window.search_window_area import SearchWindowLocationArea
from mesh_city.gui.search_window.search_window_location import SearchWindowLocation
from mesh_city.gui.widgets.button import Button as CButton
from mesh_city.gui.widgets.container import Container
from mesh_city.gui.widgets.widget_geometry import WidgetGeometry
from mesh_city.util.screen_size_util import ScreenSizeUtil


class SearchWindowStart:
	"""
	This class is a GUI element that provides the user with the type of pop-up they need to make the
	request they want to make after the request type is selected.
	"""

	def __init__(self, master, application, main_screen):
		"""
		Initializes the GUI elements for a window and prompts the user to enter what type of search
		they are interested in.
		:param master: The Tk root.
		:param application: The application object that is used to make requests.
		:param main_screen: The main screen object the popups can interact with.
		"""
		self.main_screen = main_screen
		self.master = master
		self.value = ""
		self.application = application
		self.top = Toplevel(master)

		self.top.config(padx=4)
		self.top.config(pady=4)

		self.top.attributes('-topmost', True)
		self.top.update()
		window_width, window_height, central_width, central_height = ScreenSizeUtil.get_curr_screen_geometry(520, 200)
		self.top.geometry("%dx%d+%d+%d" % (window_width, window_height, central_width, central_height))

		self.content = Container(WidgetGeometry(510, 190, 0, 0), self.top, background="white")
		layer_label_style = {"font": ("Eurostile LT Std", 18), "background": "white", "anchor": W}

		Label(
			self.content, text="What kind of search are you interested in ?", **layer_label_style,
		).place(width=510, height=40, x=0, y=0)

		CButton(
			WidgetGeometry(200, 50, 150, 50),
			"Area",
			lambda _: self.button_area_callback(),
			self.content,
		)

		CButton(
			WidgetGeometry(200, 50, 150, 120),
			"Location",
			lambda _: self.button_location_callback(),
			self.content,
		)

	def button_area_callback(self):
		"""
		Creates an area-type pop-up that in the end makes the area request to the backend.
		:return: None
		"""
		temp_window = SearchWindowLocationArea(self.master, self.application, self.main_screen)
		self.top.destroy()
		self.main_screen.master.wait_window(temp_window.top)

	def button_location_callback(self):
		"""
		Creates an location-type pop-up that in the end makes the location request to the backend.
		:return: None
		"""
		temp_window = SearchWindowLocation(self.master, self.application, self.main_screen)
		self.top.destroy()
		self.main_screen.master.wait_window(temp_window.top)
