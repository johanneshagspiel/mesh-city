"""
A module that contains the loading old request window
"""
from tkinter import Label, Toplevel, W

from mesh_city.gui.widgets.button import Button as CButton
from mesh_city.gui.widgets.container import Container
from mesh_city.gui.widgets.scrollable_container import ScrollableContainer
from mesh_city.gui.widgets.widget_geometry import WidgetGeometry


# pylint: disable=W0640
class LoadWindow:
	"""
	A window to select an old request to load onto the map
	"""

	def __init__(self, master, application, main_screen):
		"""
		The initialization method. Creates a button for each old request
		:param master: the root tkinter instance
		:param application: the global application context
		:param mainscreen: the screen from which loadwindow is called
		"""
		self.main_screen = main_screen
		self.master = master
		self.value = ""
		self.application = application
		self.image_path = self.application.file_handler.folder_overview['image_path']
		self.top = Toplevel(master)

		self.top.config(padx=4)
		self.top.config(pady=4)

		self.top.grab_set()

		self.top.geometry("%dx%d+%d+%d" % (490, 200, 0, 0))
		layer_label_style = {"font": ("Eurostile LT Std", 18), "background": "white", "anchor": W}

		self.content = Container(WidgetGeometry(480, 200, 0, 0), self.top, background="white")

		self.top_label = Label(
			self.content, text="Which request do you want to load ?", **layer_label_style,
		)
		self.top_label.place(width=470, height=40, x=0, y=0)

		self.scrollable_content = ScrollableContainer(
			WidgetGeometry(480, 140, 0, 50), self.content, background="white"
		)

		element_added = 0

		if self.application.current_request is not None:
			active_request_id = self.application.current_request.request_id

			for request in self.application.request_manager.requests:
				if request.request_id != active_request_id:
					self.scrollable_content.add_row(
						lambda parent: CButton(
						WidgetGeometry(200, 50, 120, 0),
						request.name,
						lambda _,
						request=request: self.load_request(request),
						parent
						)
					)
					element_added += 1
		else:
			for request in self.application.request_manager.requests:
				self.scrollable_content.add_row(
					lambda parent: CButton(
					WidgetGeometry(200, 50, 120, 0),
					request.name,
					lambda _,
					request=request: self.load_request(request),
					parent
					)
				)
				element_added += 1

	def load_request(self, request):
		"""
		Loads an old request as the current request into the main_screen
		:param name_directory: the directory where the request to be loaded is stored
		:return: nothing
		"""
		self.application.set_current_request(request=request)
		self.main_screen.closed_popup_successfully = True

		self.main_screen.render_dynamic_widgets()
		self.top.destroy()
