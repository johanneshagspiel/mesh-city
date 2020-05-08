from tkinter import *
from pathlib import Path
from PIL import Image, ImageTk

class self_made_map:
	temp_path = Path(__file__).parents[1]
	image_path = Path.joinpath(temp_path, 'resources', 'images')

	def __init__(self):
		self.start()

	def start(self):
		master = Tk()
		canvas = Canvas(master, width=651, height=636)
		canvas.pack()

		photo_list = self.load_images()
		self.load_images_on_map(canvas, photo_list)

		#self.concat_images()
		#large_photo = self.load_large_image()
		#self.load_large_image_on_map(canvas, large_photo)

		side_bar = Label(canvas, width=15, height=636, text="")
		canvas_side_bar = canvas.create_window(0, 0, window=side_bar)

		search_button = Button(canvas, text="Search", width=6, height=3,
		                 command=None, bg="grey")
		canvas_search_button = canvas.create_window(28, 31, window=search_button)

		search_button_2 = Button(canvas, text="Test", width=6, height=3,
		                 command=None, bg="grey")
		canvas_search_button_2 = canvas.create_window(28, 90, window=search_button_2)

		mainloop()

	def load_large_image_on_map(self, canvas, large_image):
		canvas.create_image(15, 0, anchor=NW, image=large_image)

	def load_images_on_map(self, canvas, photo_list):
		x = 15
		y = 0
		for photo in photo_list:
			canvas.create_image(x, y, anchor=NW, image=photo)
			if (x == 439):
				x = 15
				y = y + 212
			else:
				x = x + 212

	def load_images(self):
		path_list = [Path.joinpath(self.image_path, "up_left.png"),
		             Path.joinpath(self.image_path, "up_center.png"),
		             Path.joinpath(self.image_path, "up_right.png"),
		             Path.joinpath(self.image_path, "center_left.png"),
		             Path.joinpath(self.image_path, "center_center.png"),
		             Path.joinpath(self.image_path, "center_right.png"),
		             Path.joinpath(self.image_path, "down_left.png"),
		             Path.joinpath(self.image_path, "down_center.png"),
		             Path.joinpath(self.image_path, "down_right.png")]

		get_image = lambda x: Image.open(x)
		image_list = list(map(get_image, path_list))
		resize_image = lambda x : x.resize((212, 212), Image.ANTIALIAS)
		resize_image_list = list(map(resize_image, image_list))
		get_photo = lambda x : ImageTk.PhotoImage(x)
		photo_list = list(map(get_photo, resize_image_list))
		return photo_list

	def load_large_image(self):
		get_image = Image.open(Path.joinpath(self.image_path, "large_image.png"))
		resize_image = get_image.resize((636, 636), Image.ANTIALIAS)
		get_photo = ImageTk.PhotoImage(resize_image)
		return get_photo

	def concat_images(self):
		up_left = Image.open(Path.joinpath(self.image_path, "up_left.png"))
		up_center = Image.open(Path.joinpath(self.image_path, "up_center.png"))
		up_right = Image.open(Path.joinpath(self.image_path, "up_right.png"))
		center_left = Image.open(Path.joinpath(self.image_path, "center_left.png"))
		center_center = Image.open(Path.joinpath(self.image_path, "center_center.png"))
		center_right = Image.open(Path.joinpath(self.image_path, "center_right.png"))
		down_left = Image.open(Path.joinpath(self.image_path, "down_left.png"))
		down_center = Image.open(Path.joinpath(self.image_path, "down_center.png"))
		down_right = Image.open(Path.joinpath(self.image_path, "down_right.png"))

		level_0 = self.get_concat_horizontally(self.get_concat_horizontally(
			up_left, up_center), up_right)
		level_1 = self.get_concat_horizontally(self.get_concat_horizontally(
			center_left, center_center), center_right)
		level_2 = self.get_concat_horizontally(self.get_concat_horizontally(
			down_left, down_center), down_right)

		self.get_concat_vertically(self.get_concat_vertically(
			level_0, level_1), level_2).save(Path.joinpath(self.image_path,"large_image.png"))

	def get_concat_horizontally(self, image_1,image_2):
		temp = Image.new('RGB', (image_1.width + image_2.width, image_1.height))
		temp.paste(image_1, (0, 0))
		temp.paste(image_2, (image_1.width, 0))
		return temp

	def get_concat_vertically(self, image_1, image_2):
		temp = Image.new('RGB', (image_1.width, image_1.height + image_2.height))
		temp.paste(image_1, (0, 0))
		temp.paste(image_2, (0, image_1.height))
		return temp
