"""
See :class:`.SearchWindowStart`
"""

from tkinter import Button, Label, Toplevel

from mesh_city.gui.search_window.search_window_area import SearchWindowLocationArea
from mesh_city.gui.search_window.search_window_location import SearchWindowLocation


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
		Label(self.top,
			text="What kind of search are you interested in ?").grid(row=0, columnspan=3)
		Button(self.top, text="Area", command=self.button_area_callback, bg="white")\
			.grid(row=1, columnspan=1)
		Button(self.top, text="Location",
			command=self.button_location_callback, bg="white")\
			.grid(row=1, columnspan=3)

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
