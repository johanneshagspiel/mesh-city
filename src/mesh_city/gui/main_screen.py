"""
See :class:`.MainScreen`
"""

from pathlib import Path
from tkinter import Button, Canvas, Label, mainloop, NW, Tk

from PIL import Image, ImageTk

from mesh_city.gui.detection_screen.detection_screen import DetectionScreen
from mesh_city.gui.layers_window.layers_window import LayersWindow
from mesh_city.gui.load_window.load_window import LoadWindow
from mesh_city.gui.search_window.search_window_start import SearchWindowStart
from mesh_city.gui.start_screen.start_screen import StartScreen
from mesh_city.util.image_util import ImageUtil


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
		self.image_util = ImageUtil()

		self.master = Tk()
		self.master.title("Mesh City")
		self.master.geometry("710x780")

		self.master.withdraw()
		self.window = StartScreen(self.master, application)
		self.master.wait_window(self.window.top)
		self.master.deiconify()

		self.layer_active = "normal"

		self.padding_x = 60
		self.padding_y = 5
		self.image_height = 646
		self.image_width = 646

		self.image = self.load_large_image()

		# Definition of UI of main window
		self.canvas = Canvas(self.master, width=710, height=777)
		self.canvas.grid(column=3, columnspan=30, row=0, rowspan=30)

		side_bar = Label(self.canvas, width=15, height=645, text="")
		self.canvas.create_window(0, 0, window=side_bar)

		search_button = Button(
			self.canvas, text="Search", width=6, height=3, command=self.search_window, bg="grey"
		)
		self.canvas.create_window(30, 33, window=search_button)

		load_button = Button(
			self.canvas, text="Load", width=6, height=3, command=self.load_window, bg="grey"
		)
		self.canvas.create_window(30, 92, window=load_button)

		detect_button = Button(
			self.canvas, text="Detect", width=6, height=3, command=self.detect_window, bg="grey"
		)
		self.canvas.create_window(30, 151, window=detect_button)

		layers_button = Button(
			self.canvas, text="Layers", width=6, height=3, command=self.layers_window, bg="grey"
		)
		self.canvas.create_window(30, 210, window=layers_button)

		info_button = Button(self.canvas, text="Info", width=6, height=3, command=None, bg="grey")
		self.canvas.create_window(30, 269, window=info_button)

		user_button = Button(self.canvas, text="User", width=6, height=3, command=None, bg="grey")
		self.canvas.create_window(30, 328, window=user_button)


		self.load_large_image_on_map(self.image)

		mainloop()

	def get_height(self):
		"""
		The function called when pressing on the height button to get the height from pixel.
		"""
		concat_temp_path = Path.joinpath(
			self.currently_active_tile,
			"layers",
			"ahn_height",
			"concat_image_request_10_tile_0_0.png",
		)
		self.image_util.resize_image(
			path_to_temp=self.path_to_temp,
			width=self.image_width,
			height=self.image_height,
			path=concat_temp_path,
			name="test1",
		)
		self.canvas.tag_bind(self.tkinter_image, "<Button-1>", self.get_coordinates)

	def get_coordinates(self, event):
		"""
		A method to get the height at the pixels pressed on
		:param event: a mouseclick anywhere on the image
		:return: height at the pixel pressed
		"""
		xpos = event.x - self.padding_x
		ypos = event.y - self.padding_y
		height = self.application.request_manager.ahn.get_height_from_pixel(
			xpos, ypos, Path.joinpath(self.path_to_temp, "test1")
		)
		text = "Height: " + str(height)
		self.canvas.itemconfig(self.canvas_information_line_1, text=text)

	def layers_window(self):
		"""
		Creates a layers window object
		:return: Nothing
		"""
		LayersWindow(self.master, self.application, self)

	def load_window(self):
		"""
		Creates a load request window object
		:return: Nothing
		"""
		LoadWindow(self.master, self.application, self)

	def search_window(self):
		"""
		Creates a search window object
		:return: Nothing
		"""
		SearchWindowStart(self.master, self.application, self)

	def detect_window(self):
		DetectionScreen(self.master, self.application, self)

	def update_image(self):
		"""
		Calls methods needed to updates the image seen on the map
		:return: Nothing
		"""
		self.image = self.load_large_image()
		self.load_large_image_on_map(self.image)

	def load_large_image_on_map(self, large_image):
		"""
		Loads a new image onto the map
		:param large_image: the image to be loaded
		:return: nothing
		"""
		self.tkinter_image = self.canvas.create_image(
			self.padding_x, self.padding_y, anchor=NW, image=large_image
		)

	def load_large_image(self):
		"""
		Stores and resizes the image to be loaded onto the map
		:return: nothing
		"""
		get_image = Image.open(next(self.application.file_handler.folder_overview["active_image_path"][0].glob("concat_image_*")))
		resize_image = get_image.resize((self.image_width, self.image_height), Image.ANTIALIAS)
		get_photo = ImageTk.PhotoImage(resize_image)
		return get_photo
