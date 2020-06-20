"""
This module defines a custom widget type that is at the base of other custom widgets used in the GUI.
"""
from abc import ABC
from tkinter import Canvas, Misc
from typing import Any, Dict

from mesh_city.gui.widgets.widget_geometry import WidgetGeometry


class CustomWidget(Canvas, ABC):
	"""
	This class provides an interface based on a Canvas that can be used to define custom widgets.
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
		container_cnf: Dict[Any, Any] = {"background": "white", "highlightthickness": 0, **cnf}
		super().__init__(master=master, cnf=container_cnf, **kw)

		self.geometry: WidgetGeometry = geometry

		if show:
			self.place(
				width=self.geometry.width,
				height=self.geometry.height,
				x=self.geometry.x_position,
				y=self.geometry.y_position,
			)

	def show(self) -> None:
		"""
		Shows itself on the place specified by its width, height and position.
		:return:
		"""
		self.place(
			width=self.geometry.width,
			height=self.geometry.height,
			x=self.geometry.x_position,
			y=self.geometry.y_position,
		)

	def hide(self) -> None:
		"""
		Hides this widget
		:return: None
		"""
		self.place_forget()

	def redraw(self) -> None:
		"""
		Redraws this widget to reflect possible updates.
		:return: None
		"""
		self.hide()
		self.show()
