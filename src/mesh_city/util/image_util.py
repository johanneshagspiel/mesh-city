"""
See :class:`.ImageUtil`
"""

from pathlib import Path

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

	def concat_images_tile(self, image_list):
		"""
		Method to concatenate images from a list into one tile
		:param image_list: the list with the paths of all the images to be concatenated
		:return: a concatenated tile
		"""

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
			image_1=self.get_concat_horizontally(image_1=up_left, image_2=up_center), image_2=up_right
		)
		level_1 = self.get_concat_horizontally(
			image_1=self.get_concat_horizontally(image_1=center_left, image_2=center_center),
			image_2=center_right
		)
		level_2 = self.get_concat_horizontally(
			image_1=self.get_concat_horizontally(image_1=down_left, image_2=down_center),
			image_2=down_right
		)

		temp_concat_image = self.get_concat_vertically(
			image_1=self.get_concat_vertically(image_1=level_2, image_2=level_1), image_2=level_0
		)

		return temp_concat_image

	# pylint: disable=C0200
	def combine_images_list(self, image_list, iteration_amount):
		"""
		The method to concatenate all the images from a list
		:param image_list: the list with all the images to be concatenated
		:param iteration_amount: many images are in one row of the concatenated image
		:return: the concatenated image
		"""

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

		first_round = True
		temp_entry = None
		for number in range(0, len(temp_list)):

			if first_round is True:
				temp_entry = temp_list[number]
				first_round = False
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
		images = [
			up_left,
			up_center,
			up_right,
			center_left,
			center_center,
			center_right,
			down_left,
			down_center,
			down_right
		]
		result = self.concat_image_grid(3, 3, images)
		temp_name = "request_" + str(request) + "_tile_" + tile_number
		result.save(Path.joinpath(new_folder_path, "concat_image_" + temp_name + ".png"))

	# pylint: disable=E1120
	def concat_image_grid(self, width, height, images):
		"""
		Combines a given array of images into a concatenated grid of images.
		:param width: The width of the grid
		:param height: The height of the grid
		:param images: The images to concatenate. There should be width*height images to fill the grid,
	    and images should be a flattened matrix from left to right, top to bottom.
		:return: Nothing
		"""
		if len(images) != width * height:
			raise ValueError(
				"Not enough images were supplied to concatenate an image grid of the specified size"
			)
		result = images[0]
		for x_coord in range(1, width):
			result = ImageUtil.get_concat_horizontally(
				self, image_1=result, image_2=images[x_coord]
			)
		for y_coord in range(1, height):
			new_layer = images[y_coord * width]
			for x_coord in range(1, width):
				new_layer = ImageUtil.get_concat_horizontally(
					self, image_1=new_layer, image_2=images[y_coord * width + x_coord]
				)
			result = ImageUtil.get_concat_vertically(self, image_1=result, image_2=new_layer)
		return result

	def get_concat_horizontally(self, image_1, image_2):
		"""
		Combines two tile images horizontally.
		:param image_1: The left image.
		:param image_2: The right image.
		:return: The combined image.
		"""
		# TODO change in the future potentially
		temp = Image.new("RGBA", (image_1.width + image_2.width, image_1.height))
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
		# TODO change in the future potentially
		temp = Image.new("RGBA", (image_1.width, image_1.height + image_2.height))
		temp.paste(image_1, (0, 0))
		temp.paste(image_2, (0, image_1.height))
		return temp
