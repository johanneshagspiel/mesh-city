"""
See :class:`.MainScreen`
"""

from tkinter import Button, END, Frame, Label, mainloop, Text, Tk, WORD

import numpy as np
from PIL import Image

from mesh_city.gui.detection_window.detection_window import DetectionWindow
from mesh_city.gui.eco_window.eco_window import EcoWindow
from mesh_city.gui.export_window.export_window import ExportWindow
from mesh_city.gui.layers_window.layers_window import LayersWindow
from mesh_city.gui.load_window.load_window import LoadWindow
from mesh_city.gui.load_window.select_load_option import SelectLoadOption
from mesh_city.gui.mainscreen_image.canvas_image import CanvasImage
from mesh_city.gui.mainscreen_image.gif_image import GifImage
from mesh_city.gui.search_window.search_window_start import SearchWindowStart
from mesh_city.gui.start_window.start_window import StartWindow
from mesh_city.gui.tutorial_window.tutorial_window import TutorialWindow
from mesh_city.gui.user_window.user_window import UserWindow


class MainScreen:
	"""
	The main screen of the application where the map is shown as well as as all the function one
	can do on the map such as loading requests or looking at different layers
	"""

	def __init__(self, application):
		"""
		Setting up the main screen
		:param application: the global application context
		"""

		self.application = application
		self.master = Tk()

		self.master.withdraw()
		self.window = StartWindow(self.master, self.application)
		self.master.wait_window(self.window.top)
		self.master.deiconify()

		self.master.title("Mesh City")
		self.master.geometry("910x665")

		self.active_layers = []
		self.generated_content = []

		self.padding_x = 60
		self.padding_y = 5
		self.image_height = 646
		self.image_width = 646

		self.left_bar = Frame(self.master, width=52, height=665, background="white")
		self.left_bar.grid(row=0, column=0, sticky='nsew')
		self.left_bar.grid_propagate(0)

		self.search_button = Button(
			self.left_bar, text="Search", width=6, height=3, command=self.search_window, bg="white"
		)
		self.search_button.grid(row=0, column=0)

		self.load_button = Button(
			self.left_bar, text="Load", width=6, height=3, command=self.load_window, bg="white"
		)
		self.load_button.grid(row=1, column=0)

		self.detect_button = Button(
			self.left_bar, text="Detect", width=6, height=3, command=self.detect_window, bg="white"
		)
		self.detect_button.grid(row=2, column=0)

		self.layers_button = Button(
			self.left_bar, text="Layers", width=6, height=3, command=self.layers_window, bg="white"
		)
		self.layers_button.grid(row=3, column=0)

		self.eco_button = Button(
			self.left_bar, text="Eco", width=6, height=3, command=self.eco_window, bg="white"
		)
		self.eco_button.grid(row=4, column=0)

		self.export_button = Button(
			self.left_bar, text="Export", width=6, height=3, command=self.export_window, bg="white"
		)
		self.export_button.grid(row=5, column=0)

		self.user_button = Button(
			self.left_bar, text="User", width=6, height=3, command=self.user_window, bg="white"
		)
		self.user_button.grid(row=6, column=0)

		self.right_frame = Frame(self.master, width=185, background="white")
		self.right_frame.grid(row=0, column=2, sticky='nsew')
		self.right_frame.grid_propagate(0)

		self.information_general = Text(self.right_frame, width=26, height=50, wrap=WORD)
		self.information_general.configure(font=("TkDefaultFont", 9, "normal"))
		self.information_general.grid(row=0, column=0, sticky="w")
		self.information_general.insert(END, "")
		self.information_general.configure(state='disabled')
		self.information_general.bind("<Double-1>", lambda event: "break")
		self.information_general.bind("<Button-1>", lambda event: "break")
		self.information_general.config(cursor="")

		self.gif_image = Label(self.master, text="")
		self.gif_image.grid(row=0, column=1, sticky='nsew')

		self.master.columnconfigure(1, weight=1)
		self.master.rowconfigure(0, weight=1)
		self.master.rowconfigure(1, weight=1)
		self.master.rowconfigure(2, weight=1)

	def run(self):
		"""
		Runs the main loop that updates the GUI and processes user input.
		:return: None
		"""
		mvrdv_path = self.application.file_handler.folder_overview["MVRDV"]
		new_canvas_image = Image.open(mvrdv_path)
		self.set_canvas_image(new_canvas_image)

		start_up_window = self.start_up()
		self.master.wait_window(start_up_window.top)

		mainloop()

	def create_placeholder_image(self):
		"""
		Creates a plane white placeholder image of 512x512 pixels
		:return: None
		"""
		array = np.zeros([512, 512, 3], dtype=np.uint8)
		array.fill(255)
		return Image.fromarray(array)

	def export_window(self):
		"""
		Creates an export window
		:return: None
		"""
		ExportWindow(master=self.master, application=self.application, main_screen=self)

	def layers_window(self):
		"""
		Creates a layers window object
		:return: None
		"""
		LayersWindow(self.master, self.application, self)

	def load_window(self):
		"""
		Creates a load request window object
		:return: None
		"""
		SelectLoadOption(self.master, self.application, self)

	def search_window(self):
		"""
		Creates a search window object
		:return: None
		"""
		SearchWindowStart(self.master, self.application, self)

	def detect_window(self):
		"""
		Creates a detect window object
		:return: None
		"""
		DetectionWindow(self.master, self.application)

	def user_window(self):
		"""
		Creates a UserWindow object
		:return: None
		"""
		UserWindow(master=self.master, application=self.application, main_screen=self)

	def eco_window(self):
		"""
		Creates an EcoWindow object
		:return: None
		"""
		EcoWindow(master=self.master, application=self.application, main_screen=self)

	def set_canvas_image(self, image):
		"""
		Calls methods needed to updates the image seen on the map
		:return: Nothing
		"""
		new_canvas_image = CanvasImage(self.master, image)
		new_canvas_image.grid(row=0, column=1, sticky='nsew')

	def set_gif(self, image):
		"""

		:param image:
		:return:
		"""
		self.gif_image = GifImage(self.master)
		self.gif_image.load(image)
		self.gif_image.grid(row=0, column=1, sticky='nsew')

	def delete_text(self):
		"""
		Method to delete all text in the right hand side general information text field
		:return: None
		"""
		self.information_general.configure(state='normal')
		self.information_general.delete('1.0', END)
		self.information_general.insert(END, "")
		self.information_general.configure(state='disabled')

	def update_text(self, text_to_show):
		"""
		Method to update the text field on the main screen
		:return: None
		"""
		self.information_general.configure(state='normal')
		self.information_general.delete('1.0', END)
		self.information_general.insert(END, text_to_show)
		self.information_general.configure(state='disabled')

	def start_up(self):
		"""
		Method called when starting the application. Creates either tutorial window or load screen
		:return: None
		"""
		if len(self.application.request_manager.requests) == 0:
			return TutorialWindow(self.master, self.application, self)

		return LoadWindow(self.master, self.application, self)
