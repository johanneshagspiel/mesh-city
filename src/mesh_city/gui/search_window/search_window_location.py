"""
See :class:`.SearchWindowLocation`
"""
from tkinter import Entry, Label, messagebox, Toplevel, W

from mesh_city.gui.widgets.button import Button as CButton

from mesh_city.gui.search_window.preview_window import PreviewWindow
from mesh_city.gui.widgets.container import Container
from mesh_city.gui.widgets.widget_geometry import WidgetGeometry
from mesh_city.util.input_util import InputUtil


class SearchWindowLocation:
	"""
	A pop-up type GUI element that the user can fill in to make a location-type request.
	.. todo:: Make a pop-up class that this inherits from.
	"""

	def __init__(self, master, application, main_screen):
		"""
		Initializes the GUI elements of the pop-up and sets up callbacks
		:param master: The Tk root.
		:param application: The application object that is used to make requests.
		:param main_screen: The main screen object the popups interacts with.
		"""
		self.main_screen = main_screen
		self.master = master
		self.value = ""
		self.application = application
		top = self.top = Toplevel(master)

		self.top.config(padx=4)
		self.top.config(pady=4)

		self.top.geometry("%dx%d+%d+%d" % (575, 200, 0, 0))

		self.content = Container(WidgetGeometry(565, 190, 0, 0), self.top, background="white")
		layer_label_style = {"font": ("Eurostile LT Std", 18), "background": "white", "anchor": W}

		Label(self.content, text="Which area are you interested in downloading ?",
		      **layer_label_style,
		      ).place(width=560, height=40, x=0, y=0)

		Label(self.content, text="Latitude: ",
		     **layer_label_style,
		     ).place(width=200, height=40, x=0, y=40)

		self.lat_entry = Entry(self.content, width=20, bg="grey", font=("Eurostile LT Std", 18))
		self.lat_entry.place(width=360, height=40, x=200, y=40)

		Label(self.content, text="Longitude: ",
		      **layer_label_style,
		      ).place(width=200, height=40, x=0, y=80)

		self.long_entry = Entry(self.content, width=20, bg="grey", font=("Eurostile LT Std", 18))
		self.long_entry.place(width=360, height=40, x=200, y=80)

		CButton(
			WidgetGeometry(200, 50, 170, 130),
			"Confirm",
			lambda _: self.cleanup(),
			self.content,
		)

	def cleanup(self):
		"""
		Makes the location-type request and cleans up after itself by tearing down the GUI and
		effectively returning control to the main screen.
		:return: None
		"""

		list_entries = [self.lat_entry, self.long_entry, ]
		wrong_counter_list = []

		for counter, element in enumerate(list_entries, 0):
			if InputUtil.is_float(element.get()) is False:
				wrong_counter_list.append(counter)

		if len(wrong_counter_list) > 0:
			messagebox.showinfo(
				"Input Error", "All entries must be filled out with correct coordinates"
			)
			for number in wrong_counter_list:
				list_entries[number].delete(0, 'end')

		else:
			self.value = [float(self.lat_entry.get()), float(self.long_entry.get())]

			temp_window = PreviewWindow(
				main_screen=self.main_screen,
				master=self.master,
				application=self.application,
				coordinates=self.value
			)
			self.top.destroy()
			self.main_screen.master.wait_window(temp_window.top)
