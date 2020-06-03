from tkinter import Button, Label, Scale, Toplevel

class AdditionalProviderError:
	"""
	Window showing all the options what the user can do to make the area downloaded more eco-friendly
	"""

	def __init__(self, master, application, images_remaining, providers_selected):
		"""
		The initialization method
		:param master: the master tkinter object
		:param application: the global application context
		:param main_screen: the main_screen of the application
		"""
		self.images_remaining = images_remaining
		self.providers_selected = providers_selected
		self.master = master
		self.value = ""
		self.application = application
		self.top = Toplevel(master)

		self.top.config(padx=4)
		self.top.config(pady=4)

		self.top_label = Label(self.top, text="This request would exceed your quota.")
		self.top_label.grid(row=0)

		self.usage_needed = Label(self.top, text="Exceeding Images: ")
		self.usage_needed.grid(row=1)

		self.quit_button = Button(self.top, text="Quit", command=self.top.destroy())
		self.usage_needed.grid(row=3, column=0)

		self.quit_button = Button(self.top, text="Add more image providers", command=self.more_providers)
		self.usage_needed.grid(row=3, column=1)

	def more_providers(self):
		self.top.destroy()
