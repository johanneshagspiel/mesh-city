"""
See :class:`.ImageUtil`
"""

from pathlib import Path

import numpy as np
from PIL import Image


class ImageUtil:
	"""
	Collection of functions related to assembling map tile images.
	"""

	temp_path = Path(__file__).parents[1]
	path_to_temp = Path.joinpath(temp_path, "resources", "temp")

	def concat_images_tile(self, image_list):
		"""
		Method to concatenate images from a list into one tile.

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

		images = [
			up_left,
			up_center,
			up_right,
			center_left,
			center_center,
			center_right,
			down_left,
			down_center,
			down_right,
		]
		return self.concat_image_grid(3, 3, images)

	# pylint: disable=C0200
	@staticmethod
	def combine_images_list(image_list, iteration_amount):
		"""
		The method to concatenate all the images from a list.

		:param image_list: the list with all the images to be concatenated
		:param iteration_amount: how many images are in one row of the concatenated image
		:return: the concatenated image
		"""

		return ImageUtil.concat_image_grid(
			iteration_amount, int(len(image_list) / iteration_amount), image_list
		)

	# pylint: disable=E1120
	@staticmethod
	def concat_image_grid(width, height, images):
		"""
		Combines a given array of images into a concatenated grid of images.

		:param width: The width of the grid
		:param height: The height of the grid
		:param images: The images to concatenate. There should be width*height images to fill the grid,
	    and images should be a flattened matrix from left to right, bottom to top.
		:return: Nothing
		"""

		if len(images) != width * height:
			raise ValueError(
				"Not enough images were supplied to concatenate an image grid of the specified size"
			)
		result = images[0]
		for x_coord in range(1, width):
			result = ImageUtil.get_concat_horizontally(image_1=result, image_2=images[x_coord])
		for y_coord in range(1, height):
			new_layer = images[y_coord * width]
			for x_coord in range(1, width):
				new_layer = ImageUtil.get_concat_horizontally(
					image_1=new_layer, image_2=images[y_coord * width + x_coord]
				)
			result = ImageUtil.get_concat_vertically(image_1=result, image_2=new_layer)
		return result

	@staticmethod
	def get_concat_horizontally(image_1, image_2):
		"""
		Combines two tile images horizontally.

		:param image_1: The left image.
		:param image_2: The right image.
		:return: The combined image.
		"""
		image_mode = "RGBA" if image_1.mode == "RGBA" or image_2.mode == "RGBA" else "RGB"
		temp = Image.new(image_mode, (image_1.width + image_2.width, image_1.height))
		temp.paste(image_1, (0, 0))
		temp.paste(image_2, (image_1.width, 0))
		return temp

	@staticmethod
	def get_concat_vertically(image_1, image_2):
		"""
		Combines two tile images vertically.

		:param image_1: The top image.
		:param image_2: The bottom image.
		:return: Nothing.
		"""
		image_mode =  "RGBA" if image_1.mode == "RGBA" or image_2.mode == "RGBA" else "RGB"
		temp = Image.new(image_mode, (image_1.width, image_1.height + image_2.height))
		temp.paste(image_1, (0, 0))
		temp.paste(image_2, (0, image_1.height))
		return temp

	@staticmethod
	def greyscale_matrix_to_image(matrix) -> Image:
		"""
		Converts a given matrix with values 0-255 to a grayscale image.

		:param matrix: The input matrix
		:return: A greyscale PIL image corresponding to the matrix
		"""
		return Image.fromarray(np.array(object=matrix, dtype=np.uint8), "L")
