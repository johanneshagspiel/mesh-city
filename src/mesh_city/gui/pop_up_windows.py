from tkinter import Button, END, Entry, Label, Toplevel


class SearchWindow(object):

	def __init__(self, master, application, mainscreen):
		self.mainscreen = mainscreen
		self.master = master
		self.value = ""
		self.application = application
		top = self.top = Toplevel(master)

		Label(top,
			text="Please enter the following information to start collecting maps data:").grid(
			row=0, columnspan=3
			)

		Label(top, text="Latitude").grid(row=1, columnspan=1)
		Label(top, text="Longitude").grid(row=2, columnspan=1)

		self.lat_entry = Entry(top, width=20)
		self.lat_entry.grid(row=1, columnspan=3)
		self.long_entry = Entry(top, width=20)
		self.long_entry.grid(row=2, columnspan=3)

		Button(top, text="Search", command=self.cleanup).grid(row=3, columnspan=3)

	def cleanup(self):
		self.value = [float(self.lat_entry.get()), float(self.long_entry.get())]
		self.application.request_manager.make_request_for_block(self.value)
		self.mainscreen.update_Image()
		self.top.destroy()
