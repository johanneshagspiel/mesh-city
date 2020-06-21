"""
A module defining a custom button.
"""
from tkinter import ALL, Misc, PIESLICE
from typing import Any, Dict

from mesh_city.gui.widgets.custom_widget import CustomWidget
from mesh_city.gui.widgets.widget_geometry import WidgetGeometry


class Button(CustomWidget):
	"""
	A custom button type with rounded edges.
	"""
	CORNER_RADIUS = 4

	def __init__(
		self,
		geometry: WidgetGeometry,
		text: str,
		on_click: Any = None,
		master: Misc = None,
		show: bool = True,
		cnf: Dict[Any, Any] = None,
		**kw,
	) -> None:
		if cnf is None:
			cnf = {}
		super().__init__(geometry, master, show, cnf, **kw)

		self.text = text
		self.on_click = on_click
		self._draw_items("#EEEEEE")

		self.bind("<Enter>", lambda e: self._draw_items("black", "white"))
		self.bind("<Leave>", lambda e: self._draw_items("#EEEEEE"))
		self.bind("<ButtonPress-1>", lambda e: self._draw_items("#424242", "white"))
		self.bind("<ButtonRelease-1>", lambda e: self._draw_items("black", "white"))

		self.bind("<ButtonPress-1>", self.on_click)

	def _draw_items(self, color: str, text_color: str = "black") -> None:
		"""
		Renders this button with a specified button and text color
		:param color: The color of the button itself
		:param text_color: The color of the text displayed on the button
		:return: None
		"""
		corner_diameter = self.CORNER_RADIUS * 2
		right_offset = self.geometry.width - corner_diameter
		bottom_offset = self.geometry.height - corner_diameter
		style = {"fill": color, "outline": ""}

		self.delete(ALL)

		self.create_arc(0, 0, corner_diameter, corner_diameter, start=90, style=PIESLICE, **style)
		self.create_arc(
			0,
			bottom_offset,
			corner_diameter,
			self.geometry.height - 1,
			start=180,
			style=PIESLICE,
			**style
		)
		self.create_arc(
			right_offset,
			0,
			self.geometry.width - 1,
			corner_diameter,
			start=0,
			style=PIESLICE,
			**style
		)
		self.create_arc(
			right_offset,
			bottom_offset,
			self.geometry.width - 1,
			self.geometry.height - 1,
			start=270,
			style=PIESLICE,
			**style
		)
		self.create_rectangle(
			0, self.CORNER_RADIUS, self.CORNER_RADIUS, bottom_offset + self.CORNER_RADIUS, **style
		)
		self.create_rectangle(
			right_offset + self.CORNER_RADIUS,
			self.CORNER_RADIUS,
			self.geometry.width,
			bottom_offset + self.CORNER_RADIUS,
			**style
		)
		self.create_rectangle(
			self.CORNER_RADIUS, 0, right_offset + self.CORNER_RADIUS, self.geometry.height, **style
		)
		self.create_text(
			self.geometry.width / 2,
			self.geometry.height / 2,
			text=self.text,
			font=("Eurostile LT Std", 18),
			fill=text_color
		)
