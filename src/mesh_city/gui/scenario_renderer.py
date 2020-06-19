"""
See :class:`.ScenarioRenderer`
"""
import math

import cv2
import numpy as np
from geopandas import GeoDataFrame
from pandas import DataFrame
from PIL import Image, ImageDraw, ImageOps

from mesh_city.request.layers.google_layer import GoogleLayer
from mesh_city.scenario.scenario import Scenario
from mesh_city.util.image_util import ImageUtil


class ScenarioRenderer:
	"""
	A class used to create scenario's from requests whose behaviour can be customized by specifying
	what type of things it should change.
	"""

	def __init__(self, overlay_image: Image):
		self.overlay_image = overlay_image

	def render_scenario(self, scenario: Scenario, scaling: int = 16) -> Image:
		"""
		Composites a rendering of a scenario
		:param scenario: The scenario to render
		:param scaling: A scaling factor for low-resolution rendering
		:return: An image representation of the layer.
		"""
		request = scenario.request
		tiles = request.get_layer_of_type(GoogleLayer).tiles
		images = []
		for tile in tiles:
			large_image = Image.open(tile.path).convert("RGBA")
			width, height = large_image.size
			images.append(large_image.resize((round(width / scaling), round(height / scaling))))
		result_image = ImageUtil.concat_image_grid(
			width=request.num_of_horizontal_images,
			height=request.num_of_vertical_images,
			images=images
		).convert("RGBA")
		buildings = scenario.buildings.copy(deep=True)
		if scenario.buildings is not None:
			result_image = ScenarioRenderer.render_shrubbery(
				base_image=result_image, buildings=buildings, overlay_image=self.overlay_image,
				scaling=scaling
			)
		if scenario.trees is not None:
			result_image = ScenarioRenderer.render_trees(
				base_image=result_image, trees=scenario.trees, scaling=scaling
			)
		return result_image

	@staticmethod
	def render_shrubbery(base_image: Image, buildings: GeoDataFrame, overlay_image: Image,
	                     scaling=1) -> Image:
		"""
		Turns rooftops into shrubbery.
		:param base_image: The base image
		:param buildings: A dataframe with building polygons
		:param scaling: A scaling factor
		:return:
		"""
		buildings.geometry = buildings.geometry.scale(
			xfact=1 / scaling, yfact=1 / scaling, zfact=1.0, origin=(0, 0)
		)
		green_overlay = np.asarray(overlay_image)
		vertical_tiles = math.ceil(base_image.height / overlay_image.height)
		horizontal_tiles = math.ceil(base_image.width / overlay_image.width)
		tiled_overlay = np.tile(green_overlay, (vertical_tiles, horizontal_tiles, 1))
		cropped_overlay = tiled_overlay[0:base_image.height, 0:base_image.width]
		mask_base = Image.new('RGB', (base_image.width, base_image.height), (0, 0, 0))
		draw = ImageDraw.Draw(mask_base)
		for (index, (polygon, label)) in enumerate(zip(buildings["geometry"], buildings["label"])):
			if label == "Shrubbery":
				vertices = list(zip(*polygon.exterior.coords.xy))
				draw.polygon(xy=vertices, fill=(255, 255, 255))
		final_mask = np.asarray(mask_base).astype(float) / 255
		print(final_mask.shape)
		print(cropped_overlay.shape)
		final_overlay = cv2.multiply(final_mask, cropped_overlay, dtype=cv2.CV_32F)
		masked_numpy_base = cv2.multiply(
			1 - final_mask, np.asarray(base_image.convert("RGB")), dtype=cv2.CV_32F
		)
		new_base_image_numpy = cv2.add(masked_numpy_base, final_overlay, dtype=cv2.CV_8UC3)
		return Image.fromarray(new_base_image_numpy.astype(np.uint8)).convert("RGBA")

	@staticmethod
	def render_trees(base_image: Image, trees: DataFrame, scaling: int = 1):
		"""
		Adds more trees to the image based on the detected trees
		:param request: the request for which to add more trees to
		:param trees_to_add: how many trees to add
		:return:
		"""
		source_trees = trees.loc[trees['label'] == "Tree"]
		trees_to_add = trees.loc[trees['label'] != "Tree"]
		source_image = base_image.copy()
		for (index, row) in trees_to_add.iterrows():
			source_tree_index = row["source_index"]
			tree_area_to_cut = (
				float(source_trees.iloc[source_tree_index][0]) / scaling,
				float(source_trees.iloc[source_tree_index][1]) / scaling,
				float(source_trees.iloc[source_tree_index][2]) / scaling,
				float(source_trees.iloc[source_tree_index][3]) / scaling,
			)
			tree_image_cropped = source_image.crop(box=tree_area_to_cut)
			mask = Image.new('L', tree_image_cropped.size, 0)
			draw = ImageDraw.Draw(mask)
			draw.ellipse((0, 0) + tree_image_cropped.size, fill=255)
			source_tree_image = ImageOps.fit(tree_image_cropped, mask.size, centering=(0.5, 0.5))
			source_tree_image.putalpha(mask)

			coordinate = ((int(row["xmin"] / scaling), int(row["ymin"] / scaling)))
			base_image.alpha_composite(source_tree_image, dest=coordinate)
		return base_image
