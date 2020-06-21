"""
See :class:`.SearchWindowLocationArea`
"""

from tkinter import Entry, Label, messagebox, Toplevel, W

from mesh_city.gui.search_window.preview_window import PreviewWindow
from mesh_city.gui.widgets.button import Button as CButton
from mesh_city.gui.widgets.container import Container
from mesh_city.gui.widgets.widget_geometry import WidgetGeometry
from mesh_city.util.input_util import InputUtil


class SearchWindowLocationArea:
	"""
	A pop-up type GUI element that the user can fill in to make an area-type request.
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
		self.top = Toplevel(master)

		self.top.config(padx=4)
		self.top.config(pady=4)

		self.top.geometry("%dx%d+%d+%d" % (575, 280, 0, 0))

		self.content = Container(WidgetGeometry(565, 270, 0, 0), self.top, background="white")
		layer_label_style = {"font": ("Eurostile LT Std", 18), "background": "white", "anchor": W}

		Label(
			self.content, text="Which area are you interested in downloading ?", **layer_label_style,
		).place(width=560, height=40, x=0, y=0)

		Label(self.content, text="Min Latitude: ", **layer_label_style,
				).place(width=200, height=40, x=0, y=40)

		self.min_lat_entry = Entry(self.content, width=20, bg="grey", font=("Eurostile LT Std", 18))
		self.min_lat_entry.place(width=360, height=40, x=200, y=40)

		Label(self.content, text="Min Longitude: ", **layer_label_style,
				).place(width=200, height=40, x=0, y=80)

		self.min_long_entry = Entry(
			self.content, width=20, bg="grey", font=("Eurostile LT Std", 18)
		)
		self.min_long_entry.place(width=360, height=40, x=200, y=80)

		Label(self.content, text="Max Latitude: ", **layer_label_style,
				).place(width=200, height=40, x=0, y=120)

		self.max_lat_entry = Entry(self.content, width=20, bg="grey", font=("Eurostile LT Std", 18))
		self.max_lat_entry.place(width=360, height=40, x=200, y=120)

		Label(self.content, text="Max Longitude: ", **layer_label_style,
				).place(width=200, height=40, x=0, y=160)

		self.max_long_entry = Entry(
			self.content, width=20, bg="grey", font=("Eurostile LT Std", 18)
		)
		self.max_long_entry.place(width=360, height=40, x=200, y=160)

		CButton(
			WidgetGeometry(200, 50, 170, 210), "Confirm", lambda _: self.cleanup(), self.content,
		)

	def cleanup(self):
		"""
		Makes the area-type request and cleans up after itself by tearing down the GUI and
		effectively returning control to the main screen.
		"""
		list_entries = [
			self.min_lat_entry, self.min_long_entry, self.max_lat_entry, self.max_long_entry,
		]

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
			self.value = [
				float(self.min_lat_entry.get()),
				float(self.min_long_entry.get()),
				float(self.max_lat_entry.get()),
				float(self.max_long_entry.get()),
			]

			temp_window = PreviewWindow(
				main_screen=self.main_screen,
				master=self.master,
				application=self.application,
				coordinates=self.value
			)
			self.top.destroy()
			self.main_screen.master.wait_window(temp_window.top)
