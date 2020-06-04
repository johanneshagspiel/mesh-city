"""Module for creating tile dictionaries from large images that can be processed by detectors"""
from math import ceil

import numpy as np


class ImageTiler():
	def __init__(self, tile_width, tile_height):
		self.tile_width = tile_width
		self.tile_height = tile_height

	def create_tile_dictionary(self, data):
		image_width = data.shape[0]
		image_height = data.shape[1]
		assert self.tile_width <= image_width
		assert self.tile_height <= image_height
		tile_dictionary = {}
		for x in range(ceil(image_width / self.tile_width)):
			for y in range(ceil(image_height / self.tile_height)):
				upper_y = min(image_height - self.tile_height, y * self.tile_height)
				left_x = min(image_width - self.tile_width, x * self.tile_width)
				tile_dictionary[(left_x, upper_y)] = data[upper_y:upper_y + self.tile_height,
				                                     left_x:left_x + self.tile_width]
		return tile_dictionary

	def reconstruct_image_from_dict(self, tile_dictionary):
		image_width = 0
		image_height = 0
		for (x, y) in tile_dictionary:
			image_width = max(image_width, x + self.tile_width)
			image_height = max(image_height, y + self.tile_height)
		array = np.empty((image_height, image_width))
		for (x, y) in tile_dictionary:
			array[y:y + self.tile_height, x:x + self.tile_width] = tile_dictionary[(x, y)]
		return array
