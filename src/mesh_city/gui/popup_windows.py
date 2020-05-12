from tkinter import Button, Entry, Label, Toplevel


class RegisterPopupWindow(object):

	def __init__(self, master):
		self.value = ""
		top = self.top = Toplevel(master)
		Label(top,
		      text="Please enter the following information to start collecting maps data:").grid(
			row=0, columnspan=3
		)
		Label(top, text="Name").grid(row=1)
		Label(top, text="Google API key").grid(row=2)
		Label(top, text="Monthly quota").grid(row=3)
		self.name_entry = Entry(top)
		self.key_entry = Entry(top)
		self.quotum_entry = Entry(top)
		self.name_entry.grid(row=1, column=1)
		self.key_entry.grid(row=2, column=1)
		self.quotum_entry.grid(row=3, column=1)
		self.b = Button(top, text="OK", command=self.cleanup)
		self.b.grid(row=4, columnspan=3)

	def cleanup(self):
		self.value = (self.name_entry.get(), self.key_entry.get(), self.quotum_entry.get())
		self.top.destroy()


class NamePopupWindow(object):

	def __init__(self, master):
		self.value = ""
		top = self.top = Toplevel(master)
		Label(top, text="Please enter your name:").grid(row=0, columnspan=3)
		Label(top, text="Name").grid(row=1)
		self.name_entry = Entry(top)
		self.name_entry.grid(row=1, column=1)
		self.b = Button(top, text='Ok', command=self.cleanup)
		self.b.grid(row=4, columnspan=3)

	def cleanup(self):
		self.value = self.name_entry.get()
		self.top.destroy()
