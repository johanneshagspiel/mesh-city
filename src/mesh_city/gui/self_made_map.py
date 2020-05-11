from datetime import datetime
from pathlib import Path
from os import path
from tkinter import *
from tkinter import filedialog

from PIL import (
	Image,
	ImageTk,
)

from mesh_city.gui.popup_windows import (
	NamePopupWindow,
	RegisterPopupWindow,
)
from mesh_city.util.google_maps.quota_manager import QuotaManager
from mesh_city.util.google_maps.user_info import UserInfo
from mesh_city.util.google_maps.user_info_handler import UserInfoHandler
from mesh_city.util.google_maps.google_maps_entity import GoogleMapsEntity


def set_entry(entry, value):
	entry.delete(0, END)
	entry.insert(0, value)


class SelfMadeMap(object):

	def __init__(self, master):
		self.master = master
		self.file = path.dirname(__file__)
		self.image_path = Path.joinpath(Path(__file__).parents[1], 'resources', 'images')

		# Definition of UI of main window
		self.canvas = Canvas(self.master, width=651, height=636)
		self.canvas.grid(column=3, columnspan=30, row=0, rowspan=30)

		self.file_entry = Entry(self.master)
		self.file_entry.grid(row=0, columnspan=3)
		set_entry(self.file_entry, self.file)
		btn1 = Button(self.master, text="Change output folder", command=self.select_dir)
		btn1.grid(row=1, columnspan=3)

		Label(self.master, text="Quota").grid(row=2)
		Label(self.master, text="Latitude").grid(row=3)
		Label(self.master, text="Longitude").grid(row=4)

		self.lat_entry = Entry(self.master)
		self.long_entry = Entry(self.master)
		self.quota_entry = Entry(self.master)
		self.quota_entry.grid(row=2, column=1)
		self.lat_entry.grid(row=3, column=1)
		self.long_entry.grid(row=4, column=1)

		btn2 = Button(self.master, text="Extract imagery to output folder",
		              command=self.request_data)
		btn2.grid(row=5, columnspan=3)
		large_photo = self.load_large_image()
		self.load_large_image_on_map(self.canvas, large_photo)

		#####

		self.user_info_handler = UserInfoHandler()
		if self.user_info_handler.file_exists():
			self.ask_for_name()
		else:
			self.register_user()

		self.quota_manager = QuotaManager(self.user_info)
		self.maps_entity = GoogleMapsEntity(self.user_info,self.quota_manager)
		mainloop()

	def select_dir(self):
		self.file = filedialog.askdirectory(initialdir=path.dirname(__file__))
		set_entry(self.file_entry, self.file)
		print("Selected: %s" % (self.file))

	def clear_canvas(self):
		self.canvas.delete("all")

	def ask_for_name(self):
		self.user_info = self.user_info_handler.load_user_info()
		self.w = NamePopupWindow(self.master)
		self.master.wait_window(self.w.top)
		name = self.w.value

	def register_user(self):
		self.w = RegisterPopupWindow(self.master)
		self.master.wait_window(self.w.top)
		current_time = datetime.now()
		name, key, quota = self.w.value
		self.user_info = UserInfo(name, key, quota, 0, current_time.year,
		                          current_time.month, current_time.day,
		                          current_time.hour, current_time.minute,
		                          current_time.second)
		self.user_info_handler.store_user_info(self.user_info)

	def request_data(self):
		latitude, longitude = float(self.lat_entry.get()), float(self.long_entry.get())
		self.maps_entity.load_images_map(latitude, longitude)
		# photo_list = self.load_images()
		# self.load_images_on_map(self.canvas, photo_list)
		self.clear_canvas()
		self.concat_images()
		large_photo = self.load_large_image()
		self.load_large_image_on_map(self.canvas, large_photo)

	def load_large_image_on_map(self, canvas, large_image):
		canvas.create_image(15, 0, anchor=NW, image=large_image)

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
			level_0, level_1), level_2).save(
			Path.joinpath(self.image_path, "large_image.png"))

	def get_concat_horizontally(self, image_1, image_2):
		temp = Image.new('RGB', (image_1.width + image_2.width, image_1.height))
		temp.paste(image_1, (0, 0))
		temp.paste(image_2, (image_1.width, 0))
		return temp

	def get_concat_vertically(self, image_1, image_2):
		temp = Image.new('RGB', (image_1.width, image_1.height + image_2.height))
		temp.paste(image_1, (0, 0))
		temp.paste(image_2, (0, image_1.height))
		return temp
