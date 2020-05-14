from tkinter import Button, END, Entry, Label, Toplevel


class PopUpWindow:

	def __init__(self, master, application, type):
		self.value = ""
		self.master = master
		self.application = application

		top = self.top = Toplevel(master)
		top.withdraw()

		if type == "search_window":
			#SearchWindow(self.master, self.application)
			self.w = SearchWindow(self.master, self.application)
			coordinates = self.w.value
			#self.master.wait_window(self.w.top)


class SearchWindow(object):

	def __init__(self, master, application):
		self.master = master
		self.value = ""
		top = self.top = Toplevel(master)
		Label(top,
			text="Please enter the following information to start collecting maps data:").grid(
			row=0, columnspan=3
			)
		Label(top, text="Latitude").grid(row=1)
		Label(top, text="Longitude").grid(row=2)
		self.lat_entry = Entry(self.master)
		self.long_entry = Entry(self.master)
		self.quota_entry = Entry(self.master)
		self.quota_entry.grid(row=1, column=1)
		self.lat_entry.grid(row=2, column=1)

		self.b = Button(top, text="OK", command=self.cleanup)
		self.b.grid(row=3, columnspan=3)

	def cleanup(self):
		self.value = [self.lat_entry.get(), self.long_entry.get()]
		self.top.destroy()

		# self.master = master
		# self.file_entry = Entry(self.master)
		# self.file_entry.grid(row=0, columnspan=3)
		# self.set_entry(self.file_entry, self.file)
		# btn1 = Button(self.master, text="Change output folder", command=self.select_dir)
		# btn1.grid(row=1, columnspan=3)
		#
		# Label(self.master, text="Quota").grid(row=2)
		# Label(self.master, text="Latitude").grid(row=3)
		# Label(self.master, text="Longitude").grid(row=4)
		#
		# self.lat_entry = Entry(self.master)
		# self.long_entry = Entry(self.master)
		# self.quota_entry = Entry(self.master)
		# self.quota_entry.grid(row=2, column=1)
		# self.lat_entry.grid(row=3, column=1)
		# self.long_entry.grid(row=4, column=1)
		#
		# btn2 = Button(
		# 	self.master, text="Extract imagery to output folder", command=self.request_data
		# )
		# btn2.grid(row=5, columnspan=3)

	def set_entry(entry, value):
		entry.delete(0, END)
		entry.insert(0, value)

	# def select_dir(self):
	# 	self.file = filedialog.askdirectory(initialdir=path.dirname(__file__))
	# 	self.set_entry(self.file_entry, self.file)
	# 	print("Selected: %s" % self.file)
