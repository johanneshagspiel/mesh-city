"""
See :class:`.ImageUtil`
"""

from pathlib import Path

from PIL import Image


class ImageUtil:
	"""
	Collection of functions related to assembling map tile images.
	"""

	def __init__(self, resource_path=Path(__file__).parents[1].joinpath("resources")):
		self.resource_path = resource_path
		self.path_to_temp = resource_path.joinpath("temp")

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

	@staticmethod
	def concat_image_grid(width, height, images):
		"""
		Combines a given array of images into a concatenated grid of images.
		:param width: The width of the grid
		:param height: The height of the grid
		:param images: The images to concatenate. There should be width*height images to fill the grid.
		:return: Nothing
		"""
		if len(images) != width * height:
			raise ValueError(
				"Not enough images were supplied to concatenate an image grid of the specified size"
			)
		result = images[0]
		for x in range(1, width):
			result = ImageUtil.get_concat_horizontally(result, images[x])
		for y in range(1, height):
			new_layer = images[y * width]
			for x in range(1, width):
				new_layer = ImageUtil.get_concat_horizontally(result, images[y * width + x])
			result = ImageUtil.get_concat_vertically(result, new_layer)
		return result

	@staticmethod
	def get_concat_horizontally(image_1, image_2):
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

	@staticmethod
	def get_concat_vertically(image_1, image_2):
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

	def create_resized_copy(self, path_to_temp, width, height, path, name):
		"""
		Resizes a tile image to given dimensions.
		:param path_to_temp: Path for temporary files.
		:param width: The desired width in pixels.
		:param height: The desired height in pixels.
		:param path: The path of the original image.
		:param name: The filename of the new image.
		:return: Nothing.
		"""
		get_image = Image.open(path)
		resize_image = get_image.resize((width, height), Image.ANTIALIAS)
		resize_image.save(fp=Path.joinpath(path_to_temp, name), format="png")
