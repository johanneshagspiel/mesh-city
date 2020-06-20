"""
Adapted from https://stackoverflow.com/a/3092341/5280420.
"""

from tkinter import Canvas, Misc, NW, BOTH, Y, RIGHT, LEFT, SCROLL, UNITS, ALL, VERTICAL
from tkinter.ttk import Scrollbar
from typing import Dict, Any, Callable

from mesh_city.gui.widgets.container import Container
from mesh_city.gui.widgets.custom_widget import CustomWidget
from mesh_city.gui.widgets.widget_geometry import WidgetGeometry


class ScrollableContainer(Container):

    def __init__(
        self,
        geometry: WidgetGeometry,
        master: Misc = None,
        show: bool = True,
        cnf: Dict[Any, Any] = {},
        **kw,
    ) -> None:
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

    def _bind_global_scroll(self, enter_event) -> None:
        self.bind_all("<MouseWheel>", lambda scroll_event:
            self.canvas.yview(SCROLL, int(-scroll_event.delta / 30), UNITS)
        )

    def _unbind_global_scroll(self, leave_event) -> None:
        self.unbind_all("<MouseWheel>")

    def _on_frame_configure(self, event) -> None:
        """Reset the scroll region to encompass the inner frame"""

        self.canvas.configure(scrollregion=self.canvas.bbox(ALL))

    def add_row(self, partial_widget: Callable[[Misc], CustomWidget]) -> None:
        row_container = Canvas(self.frame, background="white", highlightthickness=0)
        row_widget = partial_widget(row_container)
        row_container.configure(width=self.geometry.width, height=row_widget.geometry.height)
        row_container.grid(row=self.nr_of_rows, column=0)
        self.nr_of_rows += 1
