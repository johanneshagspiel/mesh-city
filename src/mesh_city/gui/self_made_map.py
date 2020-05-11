from os import path
from tkinter import *
from pathlib import Path
from tkinter import END, NW, Button, Canvas, Entry, Label, Tk, filedialog, mainloop

from PIL import Image, ImageTk

from mesh_city.imagery_provider.user_entity import UserEntity
from mesh_city.imagery_provider.map_provider.google_maps_entity import GoogleMapsEntity


def set_entry(entry, value):
    entry.delete(0,END)
    entry.insert(0,value)


class self_made_map:

	def __init__(self, request_manager):
		self.temp_path = Path(__file__).parents[1]
		self.image_path = Path.joinpath(self.temp_path, 'resources', 'images')
		self.file = path.dirname(__file__)
		self.start()
		self.request_manager = request_manager

	def select_dir(self):
		self.file = filedialog.askdirectory(initialdir=path.dirname(__file__))
		set_entry(self.file_entry, self.file)
		print("Selected: %s" % (self.file))

	def clear_canvas(self):
		self.canvas.delete("all")

	def request_data(self):
		maps_entity = GoogleMapsEntity(UserEntity(int(self.quota_entry.get())))
		latitude, longitude = float(self.lat_entry.get()), float(self.long_entry.get())
		self.google_maps_entity.load_images_map(latitude,longitude)
		# photo_list = self.load_images()
		# self.load_images_on_map(self.canvas, photo_list)
		self.clear_canvas()
		self.concat_images()
		large_photo = self.load_large_image()
		self.load_large_image_on_map(self.canvas, large_photo)


	def start(self):
		master = Tk()
		master.title("Google maps extractor")
		master.geometry("")

		self.canvas = Canvas(master, width=651, height=636)
		self.canvas.grid(column=3,columnspan=30,row=0,rowspan=30)

		self.file_entry = Entry(master)
		self.file_entry.grid(row=0,columnspan=3)
		set_entry(self.file_entry,self.file)
		btn1 = Button(master, text="Change output folder", command=self.select_dir)
		btn1.grid(row=1,columnspan=3)

		Label(master, text="Quota").grid(row=2)
		Label(master, text="Latitude").grid(row=3)
		Label(master, text="Longitude").grid(row=4)

		self.lat_entry = Entry(master)
		self.long_entry = Entry(master)
		self.quota_entry = Entry(master)
		self.quota_entry.grid(row=2, column=1)
		self.lat_entry.grid(row=3, column=1)
		self.long_entry.grid(row=4, column=1)

		btn2 = Button(master, text="Extract imagery to output folder",
		              command=self.request_data)
		btn2.grid(row=5,columnspan=3)
		large_photo = self.load_large_image()
		self.load_large_image_on_map(self.canvas, large_photo)

		mainloop()


	def load_large_image_on_map(self, canvas, large_image):
		canvas.create_image(15, 0, anchor=NW, image=large_image)

	def load_large_image(self):
		get_image = Image.open(Path.joinpath(self.image_path, "large_image.png"))
		resize_image = get_image.resize((636, 636), Image.ANTIALIAS)
		get_photo = ImageTk.PhotoImage(resize_image)
		return get_photo

	def load_images_on_map(self, canvas, photo_list):
		x = 15
		y = 0
		for photo in photo_list:
			canvas.create_image(x, y, anchor=NW, image=photo)
			if x == 439:
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
		resize_image = lambda x: x.resize((212, 212), Image.ANTIALIAS)
		resize_image_list = list(map(resize_image, image_list))
		get_photo = lambda x: ImageTk.PhotoImage(x)
		photo_list = list(map(get_photo, resize_image_list))
		return photo_list
