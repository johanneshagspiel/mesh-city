from PIL import Image
import glob
from pathlib import Path

class ImageUtil:

	def __init__(self):
		pass

	def concat_images(self, new_folder_path, request, tile_number, type):
		name_type = NameType(type)
		up_left = Image.open(
			glob.glob(Path.joinpath(new_folder_path, name_type.names[0]).absolute().as_posix()).pop()
		)
		up_center = Image.open(
			glob.glob(Path.joinpath(new_folder_path, name_type.names[1]).absolute().as_posix()).pop()
		)
		up_right = Image.open(
			glob.glob(Path.joinpath(new_folder_path, name_type.names[2]).absolute().as_posix()).pop()
		)
		center_left = Image.open(
			glob.glob(Path.joinpath(new_folder_path, name_type.names[3]).absolute().as_posix()).pop()
		)
		center_center = Image.open(
			glob.glob(Path.joinpath(new_folder_path, name_type.names[4]).absolute().as_posix()).pop()
		)
		center_right = Image.open(
			glob.glob(Path.joinpath(new_folder_path, name_type.names[5]).absolute().as_posix()).pop()
		)
		down_left = Image.open(
			glob.glob(Path.joinpath(new_folder_path, name_type.names[6]).absolute().as_posix()).pop()
		)
		down_center = Image.open(
			glob.glob(Path.joinpath(new_folder_path, name_type.names[7]).absolute().as_posix()).pop()
		)
		down_right = Image.open(
			glob.glob(Path.joinpath(new_folder_path, name_type.names[8]).absolute().as_posix()).pop()
		)

		level_0 = self.get_concat_horizontally(
			self.get_concat_horizontally(up_left, up_center), up_right
		)
		level_1 = self.get_concat_horizontally(
			self.get_concat_horizontally(center_left, center_center), center_right
		)
		level_2 = self.get_concat_horizontally(
			self.get_concat_horizontally(down_left, down_center), down_right
		)

		request_string = str(request)
		tile_number_string = str(tile_number)
		temp_name = "request_" + request_string + "_tile_" + tile_number_string
		self.get_concat_vertically(self.get_concat_vertically(level_0, level_1),
		                           level_2).save(
			Path.joinpath(new_folder_path, "concat_image_" + temp_name + ".png"))

	def get_concat_horizontally(self, image_1, image_2):
		temp = Image.new("RGB", (image_1.width + image_2.width, image_1.height))
		temp.paste(image_1, (0, 0))
		temp.paste(image_2, (image_1.width, 0))
		return temp

	def get_concat_vertically(self, image_1, image_2):
		temp = Image.new("RGB", (image_1.width, image_1.height + image_2.height))
		temp.paste(image_1, (0, 0))
		temp.paste(image_2, (0, image_1.height))
		return temp

class NameType:

	def __init__(self, type):
		self.names = self.start(type)

	def start(self, type):
		if(type == "normal"):
			return ["1_*", "2_*", "3_*", "4_*", "5_*", "6_*", "7_*", "8_*", "9_*"]
