from tkinter import Misc
from typing import Any, Dict

from mesh_city.gui.widgets.button import Button
from mesh_city.gui.widgets.widget_geometry import WidgetGeometry


class LayerButton(Button):

	def __init__(
		self,
		geometry: WidgetGeometry,
		text: str,
		button_color: str,
		text_color: str,
		on_click: Any = None,
		master: Misc = None,
		show: bool = True,
		cnf: Dict[Any, Any] = {},
		**kw,
	) -> None:
		super().__init__(geometry, text, on_click, master, show, cnf, **kw)

		self.text = text
		self.on_click = on_click

		self._draw_items(button_color, text_color)

		self.bind("<Enter>", lambda e: self._draw_items("black", "white"))
		self.bind("<Leave>", lambda e: self._draw_items(button_color, text_color))
		self.bind("<ButtonPress-1>", lambda e: self._draw_items("#424242", "white"))
		self.bind("<ButtonRelease-1>", lambda e: self._draw_items("black", "white"))

		self.bind("<ButtonPress-1>", self.on_click)
