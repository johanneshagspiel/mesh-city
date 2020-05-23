"""
See :class:`.MainScreen`
"""

from tkinter import Button, Canvas, END, Label, mainloop, NW, Tk, Frame, Text, WORD, DISABLED, RIDGE

from PIL import Image, ImageTk

from mesh_city.gui.detection_screen.detection_screen import DetectionScreen
from mesh_city.gui.generate_screen.generate_screen import GenerateWindow
from mesh_city.gui.layers_window.layers_window import LayersWindow
from mesh_city.gui.load_window.load_window import LoadWindow
from mesh_city.gui.search_window.search_window_start import SearchWindowStart
from mesh_city.gui.start_screen.start_screen import StartScreen
from mesh_city.util.image_util import ImageUtil
from mesh_city.detection.overlay_creator import OverlayCreator


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
		self.overlay_creator = OverlayCreator(self.application, self)

		self.master = Tk()
		self.master.title("Mesh City")
		self.master.geometry("901x655")

		self.master.withdraw()
		self.window = StartScreen(self.master, application)
		self.master.wait_window(self.window.top)
		self.master.deiconify()

		self.active_layers = []

		self.padding_x = 60
		self.padding_y = 5
		self.image_height = 646
		self.image_width = 646

		self.image = self.load_large_image()

		# Definition of UI of main window
		self.canvas = Canvas(self.master, width=900, height=777)
		self.canvas.grid(column=3, row=0, rowspan=30)
		self.master.columnconfigure(3, weight=1)

		# side_bar = Label(self.canvas, width=15, height=645, information_general="")
		# self.canvas.create_window(0, 0, window=side_bar)

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

		generate_button = Button(self.canvas, text="Generate", width=6, height=3, command=self.generate_window, bg="grey")
		self.canvas.create_window(30, 269, window=generate_button)

		export_button = Button(self.canvas, text="Export", width=6, height=3, command=None, bg="grey")
		self.canvas.create_window(30, 328, window=export_button)

		user_button = Button(self.canvas, text="User", width=6, height=3, command=None, bg="grey")
		self.canvas.create_window(30, 387, window=user_button)

		self.test_frame = Frame(self.canvas, width=185, height=646)
		self.test_frame.grid_propagate(0)
		self.canvas.create_window(803, 328, window=self.test_frame)

		self.information_general = Text(self.test_frame, width=26, height=30, wrap=WORD)
		self.information_general.configure(font=("TkDefaultFont", 9, "normal"))
		self.information_general.grid(row=0, column=0, sticky ="w")
		self.information_general.insert(END, "General")
		self.information_general.config(state=DISABLED)
		self.information_general.bind("<Double-1>", lambda event: "break")
		self.information_general.bind("<Button-1>", lambda event: "break")
		self.information_general.config(cursor="")

		self.information_selection = Text(self.test_frame, width=26, height=14, wrap=WORD)
		self.information_selection.configure(font=("TkDefaultFont", 9, "normal"))
		self.information_selection.grid(row=1, column=0, sticky ="w")
		self.information_selection.insert(END, "Selection")
		self.information_selection.config(state=DISABLED)
		self.information_selection.bind("<Double-1>", lambda event: "break")
		self.information_selection.bind("<Button-1>", lambda event: "break")
		self.information_selection.config(cursor="")

		self.load_large_image_on_map(self.image)

		mainloop()

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
		"""
		Creates a detect window object
		:return:
		"""
		DetectionScreen(self.master, self.application, self)

	def generate_window(self):
		"""
		Creates a generate window object
		:return:
		"""
		GenerateWindow(self.master, self.application, self)

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
		temp_image_path = next(
			self.application.file_handler.folder_overview["active_image_path"]
			[0].glob("concat_image_*")
		)
		get_image = Image.open(temp_image_path)
		resize_image = get_image.resize((self.image_width, self.image_height), Image.ANTIALIAS)
		get_photo = ImageTk.PhotoImage(resize_image)
		return get_photo
