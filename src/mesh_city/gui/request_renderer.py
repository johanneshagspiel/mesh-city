import csv

import numpy as np
from PIL import Image
from PIL import ImageDraw

from mesh_city.request.google_layer import GoogleLayer
from mesh_city.request.trees_layer import TreesLayer
from mesh_city.util.image_util import ImageUtil


class RequestRenderer:
	"""
	A class responsible for moving data to the detection algorithm in a way they like and then
	routing the results to the appropriate classes to create useful information.
	"""

	def __init__(self):
		pass

	@staticmethod
	def render_request(request, layer_mask):
		base_image = Image.new('RGBA', (request.width * 1024, request.height * 1024),
		                       (255, 255, 255, 0))
		result_image = base_image
		for (index, mask) in enumerate(layer_mask):
			if mask:
				result_image = Image.alpha_composite(im1=result_image,im2=RequestRenderer.create_image_from_layer(request=request, index=index))
		return result_image

	@staticmethod
	def create_image_from_layer(request, index):
		"""
		Creates one overlay from the results of a detection algorithm
		:param detection_algorithm: what kind of detection algorithm created the result
		:param image_size: the size of the image used by the detection algorithm
		:return: nothing (adds the overlay to the overlay dictionary and updates main screen
		"""
		layer = request.layers[index]
		if isinstance(layer, TreesLayer):
			# TODO change image size depending on image size used for prediction
			overlays = []
			for tile in layer.tiles:
				tree_overlay = Image.new('RGBA', (1024, 1024), (255, 255, 255, 0))
				draw = ImageDraw.Draw(tree_overlay)
				with open(tile.path, newline='') as csvfile:
					spamreader = csv.reader(csvfile, delimiter=',')
					for (index, row) in enumerate(spamreader):
						if len(row) > 0 and index > 0:
							draw.rectangle(
								xy=((float(row[1]), float(row[2])), (float(row[3]), float(row[4]))),
								outline="red"
							)
				overlays.append(tree_overlay)
			concat_image = ImageUtil.concat_image_grid(width=request.width, height=request.height,
			                                           images=overlays)
			return concat_image
		elif isinstance(layer, GoogleLayer):
			tiles = layer.tiles
			images = []
			for tile in tiles:
				images.append(Image.open(tile.path))
			concat_image = ImageUtil.concat_image_grid(width=request.width, height=request.height,
			                                           images=images).convert("RGBA")
			return concat_image
		raise ValueError("The overlay could not be created")
