from tkinter import Button, Label, Toplevel

from mesh_city.gui.search_window.search_window_start import SearchWindowStart


class TutorialWindow:

	def __init__(self, master, application, main_screen):
		self.main_screen = main_screen
		self.master = master
		self.value = ""
		self.application = application
		self.image_path = self.application.file_handler.folder_overview['image_path']
		self.top = Toplevel(master)

		self.top_label = Label(
			self.top, text="It seems like this is the first time you use this application."
		)
		self.top_label.grid(row=0)

		self.search_button = Button(
			self.top, text="Click here to make your first request", command=self.cleanup, bg="white"
		)
		self.search_button.grid(row=1)

	def cleanup(self):
		temp_window = SearchWindowStart(self.master, self.application, self.main_screen)
		self.top.destroy()
		self.main_screen.master.wait_window(temp_window.top)
