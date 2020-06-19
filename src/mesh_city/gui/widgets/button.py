from tkinter import Misc, PIESLICE, ALL
from typing import Dict, Any

from mesh_city.gui.widgets.custom_widget import CustomWidget
from mesh_city.gui.widgets.widget_geometry import WidgetGeometry


class Button(CustomWidget):

    CORNER_RADIUS = 4

    def __init__(
        self,
        geometry: WidgetGeometry,
        text: str,
        master: Misc = None,
        show: bool = True,
        cnf: Dict[Any, Any] = {},
        **kw,
    ) -> None:
        super().__init__(geometry, master, show, cnf, **kw)

        self.text = text

        self._draw_items("#EEEEEE")

        self.bind("<Enter>", lambda e: self._draw_items("black", "white"))
        self.bind("<Leave>", lambda e: self._draw_items("#EEEEEE"))
        self.bind("<ButtonPress-1>", lambda e: self._draw_items("#424242", "white"))
        self.bind("<ButtonRelease-1>", lambda e: self._draw_items("black", "white"))

    def _draw_items(self, color: str, text_color: str = "black") -> None:
        corner_diameter = self.CORNER_RADIUS * 2
        right_offset = self.geometry.width - corner_diameter
        bottom_offset = self.geometry.height - corner_diameter
        style = {"fill": color, "outline": ""}

        self.delete(ALL)

        self.create_arc(0, 0, corner_diameter, corner_diameter, start=90, style=PIESLICE, **style)
        self.create_arc(0, bottom_offset, corner_diameter, self.geometry.height - 1, start=180, style=PIESLICE, **style)
        self.create_arc(right_offset, 0, self.geometry.width - 1, corner_diameter, start=0, style=PIESLICE, **style)
        self.create_arc(right_offset, bottom_offset, self.geometry.width - 1, self.geometry.height - 1, start=270, style=PIESLICE, **style)
        self.create_rectangle(0, self.CORNER_RADIUS, self.CORNER_RADIUS, bottom_offset + self.CORNER_RADIUS, **style)
        self.create_rectangle(right_offset + self.CORNER_RADIUS, self.CORNER_RADIUS, self.geometry.width, bottom_offset + self.CORNER_RADIUS, **style)
        self.create_rectangle(self.CORNER_RADIUS, 0, right_offset + self.CORNER_RADIUS, self.geometry.height, **style)
        self.create_text(self.geometry.width / 2, self.geometry.height / 2, text=self.text, font=("Eurostile LT Std", 18), fill=text_color)
