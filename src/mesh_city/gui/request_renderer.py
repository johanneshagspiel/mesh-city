"""
See :class:`.RequestRenderer`
"""
import csv
from typing import List

import geopandas as gpd
from PIL import Image, ImageDraw

from mesh_city.request.entities.request import Request
from mesh_city.request.layers.buildings_layer import BuildingsLayer
from mesh_city.request.layers.cars_layer import CarsLayer
from mesh_city.request.layers.google_layer import GoogleLayer
from mesh_city.request.layers.trees_layer import TreesLayer
from mesh_city.util.image_util import ImageUtil


class RequestRenderer:
	"""
	A class that renders requests to Pillow images.
	"""

	@staticmethod
	def render_request(request: Request, layer_mask: List[bool], scaling=4) -> Image:
		"""
		Composites a rendering of a selected number of layers of a request.
		:param request: The request to create an image for
		:param layer_mask: A boolean mask that specifies which layers to compose
		:return: An image representation of the layer.
		"""
		base_image = Image.new(
			'RGBA',
			(
			round(request.num_of_horizontal_images * 1024 / scaling),
			round(request.num_of_vertical_images * 1024 / scaling)
			), (255, 255, 255, 255)
		)
		result_image = base_image
		for (index, mask) in enumerate(layer_mask):
			if mask:
				result_image = Image.alpha_composite(
					im1=result_image,
					im2=RequestRenderer.create_image_from_layer(
					request=request, layer_index=index, scaling=scaling
					)
				)
		return result_image

	@staticmethod
	def create_image_from_layer(request: Request, layer_index: int, scaling=16) -> Image:
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
				(
				round(request.num_of_horizontal_images * 1024 / scaling),
				round(request.num_of_vertical_images * 1024 / scaling)
				), (255, 255, 255, 0)
			)
			draw = ImageDraw.Draw(tree_overlay)
			with open(layer.detections_path, newline='') as csvfile:
				csv_reader = csv.reader(csvfile, delimiter=',')
				for (index, row) in enumerate(csv_reader):
					if len(row) > 0 and index > 0:
						draw.rectangle(
							xy=(
							(float(row[1]) / scaling, float(row[2]) / scaling),
							(float(row[3]) / scaling, float(row[4]) / scaling)
							),
							outline=(34, 139, 34),
							fill=(34, 139, 34, 50)
						)
				overlays.append(tree_overlay)
			return tree_overlay
		if isinstance(layer, CarsLayer):
			# TODO change image size depending on image size used for prediction
			overlays = []
			car_overlay = Image.new(
				'RGBA',
				(
				round(request.num_of_horizontal_images * 1024 / scaling),
				round(request.num_of_vertical_images * 1024 / scaling)
				), (255, 255, 255, 0)
			)
			draw = ImageDraw.Draw(car_overlay)
			with open(layer.detections_path, newline='') as csvfile:
				csv_reader = csv.reader(csvfile, delimiter=',')
				for (index, row) in enumerate(csv_reader):
					if len(row) > 0 and index > 0:
						draw.rectangle(
							xy=(
							(float(row[1]) / scaling, float(row[2]) / scaling),
							(float(row[3]) / scaling, float(row[4]) / scaling)
							),
							outline=(0, 0, 255),
							fill=(0, 0, 255, 50)
						)
				overlays.append(car_overlay)
			return car_overlay
		if isinstance(layer, GoogleLayer):
			tiles = layer.tiles
			images = []
			for tile in tiles:
				large_image = Image.open(tile.path).convert("RGBA")
				width, height = large_image.size
				images.append(large_image.resize((round(width / scaling), round(height / scaling))))
			concat_image = ImageUtil.concat_image_grid(
				width=request.num_of_horizontal_images,
				height=request.num_of_vertical_images,
				images=images
			).convert("RGBA")
			return concat_image

		if isinstance(layer, BuildingsLayer):
			building_dataframe = gpd.read_file(layer.detections_path)
			building_dataframe.geometry = building_dataframe.geometry.scale(
				xfact=1 / scaling, yfact=1 / scaling, zfact=1.0, origin=(0, 0)
			)
			building_overlay = Image.new(
				'RGBA',
				(
				round(request.num_of_horizontal_images * 1024 / scaling),
				round(request.num_of_vertical_images * 1024 / scaling)
				), (255, 255, 255, 0)
			)
			draw = ImageDraw.Draw(building_overlay)
			for polygon in building_dataframe["geometry"]:
				draw.polygon(
					xy=list(zip(*polygon.exterior.coords.xy)), fill=(255, 0, 0, 50), outline="red"
				)
			return building_overlay
		raise ValueError("The overlay could not be created")
