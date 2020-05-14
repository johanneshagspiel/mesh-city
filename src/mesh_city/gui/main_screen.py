import glob
from os import path
from pathlib import Path
from tkinter import Button, Canvas, Label, mainloop, NW, Tk

from PIL import Image, ImageTk

from mesh_city.gui.pop_up_windows import SearchWindow
from mesh_city.gui.start_screen import StartScreen


class MainScreen:

	def __init__(self, application):

		self.application = application

		self.master = Tk()
		self.master.title("Google maps extractor")
		self.master.geometry("653x650")

		self.master.withdraw()
		StartScreen(self.master, application)
		self.master.deiconify()

		self.image = self.load_large_image()

		self.temp_path = Path(__file__).parents[1]
		self.image_path = Path.joinpath(self.temp_path, "resources", "images")
		self.file = path.dirname(__file__)

		# Definition of UI of main window
		self.canvas = Canvas(self.master, width=650, height=650)
		self.canvas.grid(column=3, columnspan=30, row=0, rowspan=30)

		side_bar = Label(self.canvas, width=15, height=645, text="")
		canvas_side_bar = self.canvas.create_window(0, 0, window=side_bar)

		search_button = Button(
			self.canvas, text="Search", width=6, height=3, command=self.search_window, bg="grey"
		)
		canvas_search_button = self.canvas.create_window(28, 31, window=search_button)

		test1_button = Button(
			self.canvas, text="Update", width=6, height=3, command=self.update_Image, bg="grey"
		)
		canvas_test1_button = self.canvas.create_window(28, 90, window=test1_button)

		test2_button = Button(self.canvas, text="Test2", width=6, height=3, command=None, bg="grey")
		canvas_test2_button = self.canvas.create_window(28, 149, window=test2_button)

		test3_button = Button(self.canvas, text="Test3", width=6, height=3, command=None, bg="grey")
		canvas_test3_button = self.canvas.create_window(28, 208, window=test3_button)

		test4_button = Button(self.canvas, text="Test4", width=6, height=3, command=None, bg="grey")
		canvas_test4_button = self.canvas.create_window(28, 267, window=test4_button)

		test5_button = Button(self.canvas, text="Test5", width=6, height=3, command=None, bg="grey")
		canvas_test5_button = self.canvas.create_window(28, 326, window=test5_button)

		test6_button = Button(self.canvas, text="Test6", width=6, height=3, command=None, bg="grey")
		canvas_test6_button = self.canvas.create_window(28, 385, window=test6_button)

		test7_button = Button(self.canvas, text="Test7", width=6, height=3, command=None, bg="grey")
		canvas_test7_button = self.canvas.create_window(28, 444, window=test7_button)

		test8_button = Button(self.canvas, text="Test8", width=6, height=3, command=None, bg="grey")
		canvas_test8_button = self.canvas.create_window(28, 503, window=test8_button)

		test9_button = Button(self.canvas, text="Test9", width=6, height=3, command=None, bg="grey")
		canvas_test9_button = self.canvas.create_window(28, 562, window=test9_button)

		test10_button = Button(
			self.canvas, text="Test10", width=6, height=3, command=None, bg="grey"
		)
		canvas_test10_button = self.canvas.create_window(28, 621, window=test10_button)

		self.load_large_image_on_map(self.image)

		mainloop()

	def update_Image(self):
		self.image = self.load_large_image()
		self.load_large_image_on_map(self.image)

	def search_window(self):
		SearchWindow(self.master, self.application, self)

	def load_large_image_on_map(self, large_image):
		self.canvas.create_image(15, 0, anchor=NW, image=large_image)

	def load_large_image(self):
		get_image = Image.open(
			glob.glob(
			Path.joinpath(self.application.request_manager.path_to_map_image,
			"concat_image_*").absolute().as_posix()
			).pop()
		)
		resize_image = get_image.resize((636, 636), Image.ANTIALIAS)
		get_photo = ImageTk.PhotoImage(resize_image)
		return get_photo

	def clear_canvas(self):
		self.canvas.delete("all")

	def get_coordinates(event):
		xpos = event.x
		ypos = event.y

	def request_data(self):
		latitude, longitude = float(self.lat_entry.get()), float(self.long_entry.get())
		self.request_manager.make_request((latitude, longitude))
		# photo_list = self.load_images()
		# self.load_images_on_map(self.canvas, photo_list)
		self.clear_canvas()
		self.concat_images()
		large_photo = self.load_large_image()
		self.load_large_image_on_map(self.canvas, large_photo)
