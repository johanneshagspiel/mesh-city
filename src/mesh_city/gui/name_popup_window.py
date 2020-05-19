"""
See :class:`.NamePopupWindow`
"""

from tkinter import Button, Entry, Label, Toplevel


class NamePopupWindow:
	"""
    A popup window class with fields for entering a name that is stored as its value.
    """

	def __init__(self, master):
		"""
		Sets up the interface of the popup.
		:param master: The TK root
		"""
		self.value = ""
		top = self.top = Toplevel(master)
		Label(top, text="Please enter your name:").grid(row=0, columnspan=3)
		Label(top, text="Name").grid(row=1)
		self.name_entry = Entry(top)
		self.name_entry.grid(row=1, column=1)
		self.button = Button(top, text="OK", command=self.cleanup)
		self.button.grid(row=4, columnspan=3)

	def cleanup(self):
		""""
		Destroys the onscreen GUI element and stores the entered value.
		"""
		self.value = self.name_entry.get()
		self.top.destroy()
