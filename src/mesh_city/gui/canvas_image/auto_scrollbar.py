"""
A module containing the autoscrollbar for the canvas image. Taken from stackoverflow
author: FooBar167
source: https://stackoverflow.com/questions/41656176/tkinter-canvas-zoom-move-pan
"""
import tkinter as tk
from tkinter import ttk


class AutoScrollbar(ttk.Scrollbar):
	""" A scrollbar that hides itself if it's not needed. Works only for grid geometry manager """

	# pylint: disable=W0221
	def set(self, lo, hi):
		if float(lo) <= 0.0 and float(hi) >= 1.0:
			self.grid_remove()
		else:
			self.grid()
			ttk.Scrollbar.set(self, lo, hi)

	def pack(self, **kw):
		"""
	    Method to rais an error if auto scrollbar is used with pack geometry manager
	    :param kw: possible arguments used with pack methods
	    :return: raises an error
	    """
		raise tk.TclError('Cannot use pack with the widget ' + self.__class__.__name__)

	def place(self, **kw):
		"""
	    Method to rais an error if auto scrollbar is used with place geometry manager
	    :param kw: possible arguments used with pack methods
	    :return: raises an error
	    """
		raise tk.TclError('Cannot use place with the widget ' + self.__class__.__name__)
