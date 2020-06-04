"""Module for creating tile dictionaries from large images that can be processed by detectors"""
from math import ceil

import numpy as np


class ImageTiler:
	"""
	A class for deconstructing a larger image into tiles and constructing larger images from tiles
	of a certain width and height.
	"""

	def __init__(self, tile_width, tile_height):
		self.tile_width = tile_width
		self.tile_height = tile_height

	def create_tile_dictionary(self, image):
		"""
		Builds a tile dictionary for an image.
		:param image: a numpy representation of an image
		:return:
		"""
		image_width = image.shape[0]
		image_height = image.shape[1]
		assert self.tile_width <= image_width
		assert self.tile_height <= image_height
		tile_dictionary = {}
		for x_coord in range(ceil(image_width / self.tile_width)):
			for y_coord in range(ceil(image_height / self.tile_height)):
				upper_y = min(image_height - self.tile_height, y_coord * self.tile_height)
				left_x = min(image_width - self.tile_width, x_coord * self.tile_width)
				tile_dictionary[(left_x, upper_y)] = image[upper_y:upper_y + self.tile_height,
					left_x:left_x + self.tile_width]
		return tile_dictionary

	def construct_image_from_tiles(self, tile_dictionary):
		"""
		Constructs an image from tiles.
		Image size is inferred from the known tile dimensions and the coordinates.
		:param tile_dictionary: a dictionary of numpy images indexed by (x,y) coordinate tuples
		:return:
		"""
		image_width = 0
		image_height = 0
		for (x_coord, y_coord) in tile_dictionary:
			image_width = max(image_width, x_coord + self.tile_width)
			image_height = max(image_height, y_coord + self.tile_height)
		array = np.empty((image_height, image_width))
		for (x_coord, y_coord) in tile_dictionary:
			array[y_coord:y_coord + self.tile_height,
				x_coord:x_coord + self.tile_width] = tile_dictionary[(x_coord, y_coord)]
		return array
