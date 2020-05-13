from tkinter import Entry, Button, Label


class Test(object):

	def _init__(self, master):
		self.file_entry = Entry(self.master)
		self.file_entry.grid(row=0, columnspan=3)
		self.set_entry(self.file_entry, self.file)
		btn1 = Button(self.master, text="Change output folder", command=self.select_dir)
		btn1.grid(row=1, columnspan=3)

		Label(self.master, text="Quota").grid(row=2)
		Label(self.master, text="Latitude").grid(row=3)
		Label(self.master, text="Longitude").grid(row=4)

		self.lat_entry = Entry(self.master)
		self.long_entry = Entry(self.master)
		self.quota_entry = Entry(self.master)
		self.quota_entry.grid(row=2, column=1)
		self.lat_entry.grid(row=3, column=1)
		self.long_entry.grid(row=4, column=1)

		btn2 = Button(
			self.master, text="Extract imagery to output folder", command=self.request_data
		)
		btn2.grid(row=5, columnspan=3)

	def set_entry(entry, value):
		entry.delete(0, END)
		entry.insert(0, value)

	def select_dir(self):
		self.file = filedialog.askdirectory(initialdir=path.dirname(__file__))
		self.set_entry(self.file_entry, self.file)
		print("Selected: %s" % self.file)
