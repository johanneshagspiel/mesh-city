"""
See :class:`.RequestRenderer`
"""
import csv
import geopandas as gpd
from typing import List

from PIL import Image, ImageDraw

from mesh_city.request.buildings_layer import BuildingsLayer
from mesh_city.request.google_layer import GoogleLayer
from mesh_city.request.request import Request
from mesh_city.request.trees_layer import TreesLayer
from mesh_city.util.image_util import ImageUtil


class RequestRenderer:
	"""
	A class that renders requests to Pillow images.
	"""

	@staticmethod
	def render_request(request: Request, layer_mask: List[bool]) -> Image:
		"""
		Composites a rendering of a selected number of layers of a request.
		:param request: The request to create an image for
		:param layer_mask: A boolean mask that specifies which layers to compose
		:return: An image representation of the layer.
		"""
		base_image = Image.new(
			'RGBA', (request.num_of_horizontal_images * 1024, request.num_of_vertical_images * 1024),
			(255, 255, 255, 0)
		)
		result_image = base_image
		for (index, mask) in enumerate(layer_mask):
			if mask:
				result_image = Image.alpha_composite(
					im1=result_image,
					im2=RequestRenderer.create_image_from_layer(request=request, layer_index=index)
				)
		return result_image

	@staticmethod
	def create_image_from_layer(request: Request, layer_index: int) -> Image:
		"""
		Creates an image from a specific layer of a request.
		:param request: The request to create an image for
		:param layer_index: The index of the layer to create an image for
		:return: An image representation of the layer.
		"""
		layer = request.layers[layer_index]
		if isinstance(layer, TreesLayer):
			# TODO change image size depending on image size used for prediction
			overlays = []
			tree_overlay = Image.new(
				'RGBA',
				(request.num_of_horizontal_images * 1024, request.num_of_vertical_images * 1024),
				(255, 255, 255, 0)
			)
			draw = ImageDraw.Draw(tree_overlay)
			with open(layer.detections_path, newline='') as csvfile:
				csv_reader = csv.reader(csvfile, delimiter=',')
				for (index, row) in enumerate(csv_reader):
					if len(row) > 0 and index > 0:
						draw.rectangle(
							xy=((float(row[1]), float(row[2])), (float(row[3]), float(row[4]))),
							outline="red"
						)
				overlays.append(tree_overlay)
			return tree_overlay
		if isinstance(layer, GoogleLayer):
			tiles = layer.tiles
			images = []
			for tile in tiles:
				images.append(Image.open(tile.path).convert("RGBA"))
			concat_image = ImageUtil.concat_image_grid(
				width=request.num_of_horizontal_images,
				height=request.num_of_vertical_images,
				images=images
			).convert("RGBA")
			return concat_image

		if isinstance(layer, BuildingsLayer):

			building_dataframe = gpd.read_file(layer.detections_path)
			building_overlay = Image.new(
				'RGBA',
				(request.num_of_horizontal_images * 1024, request.num_of_vertical_images * 1024),
				(255, 255, 255, 0)
			)
			draw = ImageDraw.Draw(building_overlay)
			for polygon in building_dataframe["geometry"]:
				draw.polygon(xy=list(zip(*polygon.exterior.coords.xy)),outline="red")
			return building_overlay
		raise ValueError("The overlay could not be created")
