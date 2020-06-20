"""
This module defines a scrollable GUI container element.
Adapted from https://stackoverflow.com/a/3092341/5280420.
"""

from tkinter import ALL, BOTH, Canvas, LEFT, Misc, NW, RIGHT, SCROLL, UNITS, VERTICAL, Y
from tkinter.ttk import Scrollbar
from typing import Any, Callable, Dict

from mesh_city.gui.widgets.container import Container
from mesh_city.gui.widgets.custom_widget import CustomWidget
from mesh_city.gui.widgets.widget_geometry import WidgetGeometry


class ScrollableContainer(Container):
	"""
	A scrollable container that can be configured like other CustomWidget's
	"""

	def __init__(
		self,
		geometry: WidgetGeometry,
		master: Misc = None,
		show: bool = True,
		cnf: Dict[Any, Any] = None,
		**kw,
	) -> None:
		if cnf is None:
			cnf = {}
		super().__init__(geometry, master, show, cnf, **kw)

		self.canvas = Canvas(self, borderwidth=0, background="white", highlightthickness=0)
		self.frame = Canvas(self.canvas, background="white", highlightthickness=0)
		self.vsb = Scrollbar(self, orient=VERTICAL, command=self.canvas.yview)
		self.nr_of_rows = 0

		self.canvas.configure(yscrollcommand=self.vsb.set)
		self.vsb.pack(side=RIGHT, fill=Y)
		self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
		self.canvas.create_window((0, 0), window=self.frame, anchor=NW, tags="self.frame")
		self.frame.bind("<Configure>", self._on_frame_configure)

		self.bind("<Enter>", self._bind_global_scroll)
		self.bind("<Leave>", self._unbind_global_scroll)

	def _bind_global_scroll(self, _) -> None:
		"""
		Binds mouse scroll events to scrolling the canvas.
		:param _: Unused interface parameter
		:return: None
		"""
		self.bind_all(
			"<MouseWheel>",
			lambda scroll_event: self.canvas.yview(SCROLL, int(-scroll_event.delta / 30), UNITS)
		)

	def _unbind_global_scroll(self, _) -> None:
		"""
		Unbinds mousewheel events from this container.
		:param _: Unused interface parameter
		:return: None
		"""
		self.unbind_all("<MouseWheel>")

	def _on_frame_configure(self, _) -> None:
		"""
		Reset the scroll region to encompass the inner frame
		:param _: Unused interface parameter
		:return: None
		"""

		self.canvas.configure(scrollregion=self.canvas.bbox(ALL))

	def add_row(self, partial_widget: Callable[[Misc], CustomWidget]) -> None:
		"""
		Adds a widget to this container and adds a corresponding row
		:param partial_widget: The partially defined widget to add.
		:return: None
		"""
		row_container = Canvas(self.frame, background="white", highlightthickness=0)
		row_widget = partial_widget(row_container)
		row_container.configure(width=self.geometry.width, height=row_widget.geometry.height)
		row_container.grid(row=self.nr_of_rows, column=0)
		self.nr_of_rows += 1
