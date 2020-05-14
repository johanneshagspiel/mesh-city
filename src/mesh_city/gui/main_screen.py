import glob
from os import path
from pathlib import Path
from tkinter import Button, Canvas, Label, mainloop, NW, Tk

from PIL import Image, ImageTk

from mesh_city.gui.search_window import SearchWindowStart
from mesh_city.gui.start_screen import StartScreen
from mesh_city.gui.load_window import LoadWindow


class MainScreen:

	def __init__(self, application):
		self.application = application

		self.master = Tk()
		self.master.title("Mesh City")
		self.master.geometry("653x754")

		self.master.withdraw()
		StartScreen(self.master, application)
		self.master.deiconify()

		self.currently_active_image = self.application.request_manager.path_to_map_image
		self.currently_active_request = Path(self.currently_active_image).parents[0]
		print(self.currently_active_request)
		self.file = path.dirname(__file__)

		self.image = self.load_large_image()

		# Definition of UI of main window
		self.canvas = Canvas(self.master, width=650, height=753)
		self.canvas.grid(column=3, columnspan=30, row=0, rowspan=30)

		side_bar = Label(self.canvas, width=15, height=645, text="")
		canvas_side_bar = self.canvas.create_window(0, 0, window=side_bar)

		search_button = Button(
			self.canvas, text="Search", width=6, height=3, command=self.search_window, bg="grey"
		)
		canvas_search_button = self.canvas.create_window(28, 31, window=search_button)

		load_button = Button(
			self.canvas, text="Load", width=6, height=3, command=self.load_window, bg="grey"
		)
		canvas_load_button = self.canvas.create_window(28, 90, window=load_button)

		height_button = Button(self.canvas, text="Height", width=6, height=3, command=None, bg="grey")
		canvas_height_button = self.canvas.create_window(28, 149, window=height_button)

		layers_button = Button(self.canvas, text="Layers", width=6, height=3, command=None, bg="grey")
		canvas_layers_button = self.canvas.create_window(28, 208, window=layers_button)
		#
		# test4_button = Button(self.canvas, text="Test4", width=6, height=3, command=None, bg="grey")
		# canvas_test4_button = self.canvas.create_window(28, 267, window=test4_button)
		#
		# test5_button = Button(self.canvas, text="Test5", width=6, height=3, command=None, bg="grey")
		# canvas_test5_button = self.canvas.create_window(28, 326, window=test5_button)
		#
		# test6_button = Button(self.canvas, text="Test6", width=6, height=3, command=None, bg="grey")
		# canvas_test6_button = self.canvas.create_window(28, 385, window=test6_button)
		#
		# test7_button = Button(self.canvas, text="Test7", width=6, height=3, command=None, bg="grey")
		# canvas_test7_button = self.canvas.create_window(28, 444, window=test7_button)
		#
		# test8_button = Button(self.canvas, text="Test8", width=6, height=3, command=None, bg="grey")
		# canvas_test8_button = self.canvas.create_window(28, 503, window=test8_button)
		#
		# test9_button = Button(self.canvas, text="Test9", width=6, height=3, command=None, bg="grey")
		# canvas_test9_button = self.canvas.create_window(28, 562, window=test9_button)

		up_arrow = Button(
			self.canvas, text="Up", width=6, height=3, command=lambda : self.arrow("up"), bg="grey"
		)
		canvas_up_arrow = self.canvas.create_window(560, 665, window=up_arrow)

		right_arrow = Button(
			self.canvas, text="Right", width=6, height=3, command=lambda : self.arrow("right"), bg="grey"
		)
		canvas_right_arrow = self.canvas.create_window(613, 694.5, window=right_arrow)

		down_arrow = Button(
			self.canvas, text="Down", width=6, height=3, command=lambda : self.arrow("down"), bg="grey"
		)
		canvas_down_arrow = self.canvas.create_window(560, 724, window=down_arrow)

		left_arrow = Button(
			self.canvas, text="Left", width=6, height=3, command=lambda : self.arrow("left"), bg="grey"
		)
		canvas_left_arrow = self.canvas.create_window(507, 694.5, window=left_arrow)

		self.load_large_image_on_map(self.image)

		mainloop()

	def arrow(self, type):
		return None

	def load_window(self):
		LoadWindow(self.master, self.application, self)

	def search_window(self):
		SearchWindowStart(self.master, self.application, self)

	def update_Image(self):
		self.image = self.load_large_image()
		self.load_large_image_on_map(self.image)

	def load_large_image_on_map(self, large_image):
		self.canvas.create_image(15, 0, anchor=NW, image=large_image)

	def load_large_image(self):
		get_image = Image.open(
			glob.glob(
			Path.joinpath(self.currently_active_image,
			"concat_image_*").absolute().as_posix()
			).pop()
		)
		resize_image = get_image.resize((636, 636), Image.ANTIALIAS)
		get_photo = ImageTk.PhotoImage(resize_image)
		return get_photo

	def get_coordinates(event):
		xpos = event.x
		ypos = event.y
