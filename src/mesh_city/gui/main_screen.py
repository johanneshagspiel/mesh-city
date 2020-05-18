import glob
from os import path
from pathlib import Path
from tkinter import Button, Canvas, Label, mainloop, NW, Tk

from PIL import Image, ImageTk

from mesh_city.gui.layers_window import LayersWindow
from mesh_city.gui.load_window import LoadWindow
from mesh_city.gui.search_window import SearchWindowStart
from mesh_city.gui.start_screen import StartScreen
from mesh_city.gui.load_window import LoadWindow
from mesh_city.gui.layers_window import LayersWindow
from mesh_city.util.image_util import ImageUtil


class MainScreen:

	def __init__(self, application):
		self.application = application

		self.master = Tk()
		self.master.title("Mesh City")
		self.master.geometry("706x754")

		self.master.withdraw()
		StartScreen(self.master, application)
		self.master.deiconify()

		self.temp_path = Path(__file__).parents[1]
		self.path_to_temp = Path.joinpath(self.temp_path, "resources", "temp")
		self.currently_active_tile = self.application.request_manager.active_tile_path
		self.currently_active_request = Path(self.currently_active_tile).parents[0]


		self.layer_active = False
		self.padding_x = 60
		self.padding_y = 5
		self.image_height = 646
		self.image_width = 646

		self.image = self.load_large_image()

		# Definition of UI of main window
		self.canvas = Canvas(self.master, width=710, height=777)
		self.canvas.grid(column=3, columnspan=30, row=0, rowspan=30)

		side_bar = Label(self.canvas, width=15, height=645, text="")
		canvas_side_bar = self.canvas.create_window(0, 0, window=side_bar)

		search_button = Button(
			self.canvas, text="Search", width=6, height=3, command=self.search_window, bg="grey"
		)
		canvas_search_button = self.canvas.create_window(30, 33, window=search_button)

		load_button = Button(
			self.canvas, text="Load", width=6, height=3, command=self.load_window, bg="grey"
		)
		canvas_load_button = self.canvas.create_window(30, 92, window=load_button)

		layers_button = Button(self.canvas, text="Layers", width=6, height=3, command=self.layers_window, bg="grey")
		canvas_layers_button = self.canvas.create_window(30, 151, window=layers_button)

		height_button = Button(self.canvas, text="Height", width=6, height=3, command=self.get_height, bg="grey")
		canvas_height_button = self.canvas.create_window(30, 210, window=height_button)

		test4_button = Button(self.canvas, text="Test4", width=6, height=3, command=None, bg="grey")
		canvas_test4_button = self.canvas.create_window(30, 269, window=test4_button)

		test5_button = Button(self.canvas, text="Test5", width=6, height=3, command=None, bg="grey")
		canvas_test5_button = self.canvas.create_window(30, 328, window=test5_button)

		test6_button = Button(self.canvas, text="Test6", width=6, height=3, command=None, bg="grey")
		canvas_test6_button = self.canvas.create_window(30, 387, window=test6_button)

		test7_button = Button(self.canvas, text="Test7", width=6, height=3, command=None, bg="grey")
		canvas_test7_button = self.canvas.create_window(30, 446, window=test7_button)

		test8_button = Button(self.canvas, text="Test8", width=6, height=3, command=None, bg="grey")
		canvas_test8_button = self.canvas.create_window(30, 505, window=test8_button)

		test9_button = Button(self.canvas, text="Test9", width=6, height=3, command=None, bg="grey")
		canvas_test9_button = self.canvas.create_window(30, 564, window=test9_button)

		test10_button = Button(self.canvas, text="Test10", width=6, height=3, command=None, bg="grey")
		canvas_test10_button = self.canvas.create_window(30, 623, window=test10_button)

		up_arrow = Button(
			self.canvas, text="Up", width=6, height=3, command=lambda : self.arrow("up"), bg="grey"
		)
		canvas_up_arrow = self.canvas.create_window(560, 685, window=up_arrow)

		right_arrow = Button(
			self.canvas, text="Right", width=6, height=3, command=lambda : self.arrow("right"), bg="grey"
		)
		canvas_right_arrow = self.canvas.create_window(613, 714.5, window=right_arrow)

		down_arrow = Button(
			self.canvas, text="Down", width=6, height=3, command=lambda : self.arrow("down"), bg="grey"
		)
		canvas_down_arrow = self.canvas.create_window(560, 744, window=down_arrow)

		left_arrow = Button(
			self.canvas, text="Left", width=6, height=3, command=lambda : self.arrow("left"), bg="grey"
		)
		canvas_left_arrow = self.canvas.create_window(507, 714.5, window=left_arrow)

		zoom_in_button = Button(
			self.canvas, text="In", width=6, height=3, command=None, bg="grey"
		)
		canvas_zoom_in_button = self.canvas.create_window(430, 685, window=zoom_in_button)

		zoom_out_button = Button(
			self.canvas, text="Out", width=6, height=3, command=None, bg="grey"
		)
		canvas_zoom_out_button = self.canvas.create_window(430, 744, window=zoom_out_button)

		self.canvas_information_line_1 = self.canvas.create_text(195, 670, text="INFOINFOINFOINFOINFOINFOINFOINFOINFOINFO")
		self.canvas_information_line_2 = self.canvas.create_text(195, 690, text="INFOINFOINFOINFOINFOINFOINFOINFOINFOINFO")
		self.canvas_information_line_3 = self.canvas.create_text(195, 710, text="INFOINFOINFOINFOINFOINFOINFOINFOINFOINFO")
		self.canvas_information_line_4 = self.canvas.create_text(195, 730, text="INFOINFOINFOINFOINFOINFOINFOINFOINFOINFO")
		self.canvas_information_line_5 = self.canvas.create_text(195, 750, text="INFOINFOINFOINFOINFOINFOINFOINFOINFOINFO")




		self.load_large_image_on_map(self.image)

		mainloop()

	def get_height(self):
		concat_temp_path = Path.joinpath(self.currently_active_tile, "layers", "ahn_height",
		              "concat_image_request_10_tile_0_0.png",)
		ImageUtil.resize_image(self, width=self.image_width, height=self.image_height, path=concat_temp_path, name="test1")
		self.canvas.tag_bind(self.tkinter_image, "<Button-1>", self.get_coordinates)

	def get_coordinates(self, event):
		xpos = event.x - self.padding_x
		ypos = event.y - self.padding_y
		height = self.application.request_manager.ahn.get_height_from_pixel(
			xpos, ypos, Path.joinpath(self.path_to_temp, "test1")
		)
		text = "Height: " + str(height)
		self.canvas.itemconfig(self.canvas_information_bar, text=text)

	def arrow(self, type):
		return None

	def layers_window(self):
		LayersWindow(self.master, self.application, self)

	def load_window(self):
		LoadWindow(self.master, self.application, self)

	def search_window(self):
		SearchWindowStart(self.master, self.application, self)

	def update_Image(self):
		self.image = self.load_large_image()
		self.load_large_image_on_map(self.image)

	def load_large_image_on_map(self, large_image):
		self.tkinter_image = self.canvas.create_image(
			self.padding_x, self.padding_y, anchor=NW, image=large_image
		)

	def load_large_image(self):
		get_image = Image.open(
			glob.glob(
			Path.joinpath(self.currently_active_tile, "concat_image_*").absolute().as_posix()
			).pop()
		)
		resize_image = get_image.resize((self.image_width, self.image_height), Image.ANTIALIAS)
		get_photo = ImageTk.PhotoImage(resize_image)
		return get_photo
