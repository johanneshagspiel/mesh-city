import glob
from datetime import datetime
from os import path
from pathlib import Path
from tkinter import Button, Canvas, END, Entry, filedialog, Label, mainloop, NW, Tk

from PIL import Image, ImageTk

from mesh_city.gui.popup_windows import NamePopupWindow, RegisterPopupWindow
from mesh_city.imagery_provider.request_manager import RequestManager
from mesh_city.user.quota_manager import QuotaManager
from mesh_city.user.user_info import UserInfo
from mesh_city.user.user_info_handler import UserInfoHandler


def set_entry(entry, value):
	entry.delete(0, END)
	entry.insert(0, value)


class Application:

	def __init__(self):
		self.master = Tk()
		self.temp_path = Path(__file__).parents[1]
		self.image_path = Path.joinpath(self.temp_path, "resources", "images")
		self.file = path.dirname(__file__)
		self.master.title("Google maps extractor")
		self.master.geometry("")

		# Definition of UI of main window
		self.canvas = Canvas(self.master, width=651, height=650)
		self.canvas.grid(column=3, columnspan=30, row=0, rowspan=30)

		side_bar = Label(self.canvas, width=15, height=645, text="")
		canvas_side_bar = self.canvas.create_window(0, 0, window=side_bar)

		search_button = Button(
			self.canvas, text="Search", width=6, height=3, command=None, bg="grey"
		)
		canvas_search_button = self.canvas.create_window(28, 31, window=search_button)

		test1_button = Button(self.canvas, text="Test1", width=6, height=3, command=None, bg="grey")
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

		# self.file_entry = Entry(self.master)
		# self.file_entry.grid(row=0, columnspan=3)
		# set_entry(self.file_entry, self.file)
		# btn1 = Button(self.master, text="Change output folder", command=self.select_dir)
		# btn1.grid(row=1, columnspan=3)
		#
		# Label(self.master, text="Quota").grid(row=2)
		# Label(self.master, text="Latitude").grid(row=3)
		# Label(self.master, text="Longitude").grid(row=4)
		#
		# self.lat_entry = Entry(self.master)
		# self.long_entry = Entry(self.master)
		# self.quota_entry = Entry(self.master)
		# self.quota_entry.grid(row=2, column=1)
		# self.lat_entry.grid(row=3, column=1)
		# self.long_entry.grid(row=4, column=1)
		#
		# btn2 = Button(
		# 	self.master, text="Extract imagery to output folder", command=self.request_data
		# )
		# btn2.grid(row=5, columnspan=3)

		self.user_info_handler = UserInfoHandler()
		if self.user_info_handler.file_exists():
			self.ask_for_name()
		else:
			self.register_user()

		self.quota_manager = QuotaManager(self.user_info)
		self.request_manager = RequestManager(
			user_info=self.user_info, quota_manager=self.quota_manager
		)

		large_photo = self.load_large_image()
		self.load_large_image_on_map(self.canvas, large_photo)

		mainloop()

	def select_dir(self):
		self.file = filedialog.askdirectory(initialdir=path.dirname(__file__))
		set_entry(self.file_entry, self.file)
		print("Selected: %s" % self.file)

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
		self.user_info = UserInfo(
			name,
			key,
			quota,
			0,
			current_time.year,
			current_time.month,
			current_time.day,
			current_time.hour,
			current_time.minute,
			current_time.second,
		)
		self.user_info_handler.store_user_info(self.user_info)

	def request_data(self):
		latitude, longitude = float(self.lat_entry.get()), float(self.long_entry.get())
		self.request_manager.make_request((latitude, longitude))
		# photo_list = self.load_images()
		# self.load_images_on_map(self.canvas, photo_list)
		self.clear_canvas()
		self.concat_images()
		large_photo = self.load_large_image()
		self.load_large_image_on_map(self.canvas, large_photo)

	def load_large_image_on_map(self, canvas, large_image):
		canvas.create_image(15, 0, anchor=NW, image=large_image)

	def load_large_image(self):
		get_image = Image.open(
			glob.glob(
			Path.joinpath(self.request_manager.path_to_map_image,
			"concat_image_*").absolute().as_posix()
			).pop()
		)
		resize_image = get_image.resize((636, 636), Image.ANTIALIAS)
		get_photo = ImageTk.PhotoImage(resize_image)
		return get_photo
