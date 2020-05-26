"""
See :class:`.ImageUtil`
"""

from pathlib import Path
import os
from PIL import Image


class ImageUtil:
	"""
	Collection of functions related to assembling map tile images.
	"""

	# def __init__(self, application):
	# 	self.application = application
	# 	self.file_handler = self.application.file_handler

	temp_path = Path(__file__).parents[1]
	path_to_temp = Path.joinpath(temp_path, "resources", "temp")

	def concat_images_list(self, image_list):

		up_left = Image.open(image_list[0])
		up_center = Image.open(image_list[1])
		up_right = Image.open(image_list[2])
		center_left = Image.open(image_list[3])
		center_center = Image.open(image_list[4])
		center_right = Image.open(image_list[5])
		down_left = Image.open(image_list[6])
		down_center = Image.open(image_list[7])
		down_right = Image.open(image_list[8])

		level_0 = self.get_concat_horizontally(
			self.get_concat_horizontally(up_left, up_center), up_right
		)
		level_1 = self.get_concat_horizontally(
			self.get_concat_horizontally(center_left, center_center), center_right
		)
		level_2 = self.get_concat_horizontally(
			self.get_concat_horizontally(down_left, down_center), down_right
		)

		temp_concat_image = self.get_concat_vertically(self.get_concat_vertically(level_2, level_1),
			level_0)

		return temp_concat_image

	def combine_images_list(self, image_list, iteration_amount):

		temp_list = []
		temp_entry = None
		counter = 0

		for number in range(0, len(image_list)):

			if counter == 0:
				temp_entry = image_list[number]
				counter += 1
			else:
				new_temp_1 = image_list[number]
				new_temp = self.get_concat_horizontally(temp_entry, new_temp_1)
				temp_entry = new_temp
				counter += 1

			if counter % iteration_amount == 0:
				temp_list.insert(0, temp_entry)
				counter = 0

		first_Round = True
		temp_entry = None
		for number in range(0, len(temp_list)):

			if first_Round is True:
				temp_entry = temp_list[number]
				first_Round = False
			else:
				new_temp = self.get_concat_vertically(temp_entry, temp_list[number])
				temp_entry = new_temp

		return temp_entry

	def concat_images(self, new_folder_path, request, tile_number):
		"""
		Combines nine tile images into one.
		:param new_folder_path: The directory containing the tile images
		:param request: The number of the request
		:param tile_number: The lat/long identification of this tile
		:return: Nothing
		"""

		up_left = Image.open(next(new_folder_path.glob("1_*")))
		up_center = Image.open(next(new_folder_path.glob("2_*")))
		up_right = Image.open(next(new_folder_path.glob("3_*")))
		center_left = Image.open(next(new_folder_path.glob("4_*")))
		center_center = Image.open(next(new_folder_path.glob("5_*")))
		center_right = Image.open(next(new_folder_path.glob("6_*")))
		down_left = Image.open(next(new_folder_path.glob("7_*")))
		down_center = Image.open(next(new_folder_path.glob("8_*")))
		down_right = Image.open(next(new_folder_path.glob("9_*")))

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
		temp_name = "request_" + request_string + "_tile_" + tile_number
		temp_path = Path.joinpath(new_folder_path, "concat_image_" + temp_name + ".png")

		self.get_concat_vertically(self.get_concat_vertically(level_2, level_1),
			level_0).save(temp_path)

		return temp_path

	def get_concat_horizontally(self, image_1, image_2):
		"""
		Combines two tile images horizontally.
		:param image_1: The left image.
		:param image_2: The right image.
		:return: The combined image.
		"""
		temp = Image.new("RGB", (image_1.width + image_2.width, image_1.height))
		temp.paste(image_1, (0, 0))
		temp.paste(image_2, (image_1.width, 0))
		return temp

	def get_concat_vertically(self, image_1, image_2):
		"""
		Combines two tile images vertically.
		:param image_1: The top image.
		:param image_2: The bottom image.
		:return: Nothing.
		"""
		temp = Image.new("RGB", (image_1.width, image_1.height + image_2.height))
		temp.paste(image_1, (0, 0))
		temp.paste(image_2, (0, image_1.height))
		return temp

	# def make_max_image(self):
	#
	# 	tiles = (file for file in os.listdir(self.file_handler.folder_overview["active_request_path"][0])
	# 	         if os.path.isfile(os.path.join(self.file_handler.folder_overview["active_request_path"][0], file)))
	#
	# 	for tile in tiles:
	# 		return None

