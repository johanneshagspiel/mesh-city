from abc import ABC
from tkinter import Canvas, Misc
from typing import Dict, Any

from mesh_city.gui.widgets.widget_geometry import WidgetGeometry


class CustomWidget(Canvas, ABC):

    def __init__(
        self,
        geometry: WidgetGeometry,
        master: Misc = None,
        show: bool = True,
        cnf: Dict[Any, Any] = {},
        **kw,
    ) -> None:
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
        self.place(
            width=self.geometry.width,
            height=self.geometry.height,
            x=self.geometry.x_position,
            y=self.geometry.y_position,
        )

    def hide(self) -> None:
        self.place_forget()
