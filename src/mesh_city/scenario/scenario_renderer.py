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
	This renders scenario's, either per-tile or to a single (scaled-down) image.
	"""

	@staticmethod
	def render_scenario(scenario: Scenario, overlay_image: Image, scaling: int = 16) -> Image:
		"""
		Composites a rendering of a scenario based on the modified detection files.
		:param scenario: The scenario to render
		:param scaling: A scaling factor for varying the resolution of the rendered image.
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
		if scenario.trees is not None:
			result_image = ScenarioRenderer.render_trees(
				base_image=result_image, trees=scenario.trees, scaling=scaling
			)
		if scenario.buildings is not None:
			buildings = scenario.buildings.copy(deep=True)
			result_image = ScenarioRenderer.render_shrubbery(
				base_image=result_image,
				buildings=buildings,
				overlay_image=overlay_image,
				scaling=scaling
			)
		return result_image

	@staticmethod
	def render_shrubbery(
		base_image: Image, buildings: GeoDataFrame, overlay_image: Image, scaling=1
	) -> Image:
		"""
		Renders patches of shrubbery on buildings on a base image as specified in the buildings dataframe
		:param base_image: The base image
		:param buildings: A dataframe with building polygons
		:param scaling: A scaling factor for varying the resolution of the rendered image.
		:return: The resulting image
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
		for (_, (polygon, label)) in enumerate(zip(buildings["geometry"], buildings["label"])):
			if label == "Shrubbery":
				vertices = list(zip(*polygon.exterior.coords.xy))
				draw.polygon(xy=vertices, fill=(255, 255, 255))
		final_mask = np.asarray(mask_base).astype(float) / 255
		final_overlay = cv2.multiply(final_mask, cropped_overlay, dtype=cv2.CV_32F)
		masked_numpy_base = cv2.multiply(
			1 - final_mask, np.asarray(base_image.convert("RGB")), dtype=cv2.CV_32F
		)
		new_base_image_numpy = cv2.add(masked_numpy_base, final_overlay, dtype=cv2.CV_8UC3)
		return Image.fromarray(new_base_image_numpy.astype(np.uint8)).convert("RGBA")

	@staticmethod
	def render_trees_for_tile(base_image: Image, trees: DataFrame, tree_crops: [Image]) -> Image:
		"""
		Renders trees on top of a tile image based on new trees in a dataframe.
		A collection of cropped images from other tiles is used to render the new trees.
		:param base_image: The image to render the trees onto
		:param trees: A dataframe containing all the trees
		:param tree_crops: A collection of processed images of tree to use for rendering new trees.
		:return: The resulting image
		"""
		trees_to_add = trees.loc[trees['label'] != "Tree"]
		source_image = base_image.copy()
		for (_, row) in trees_to_add.iterrows():
			new_width = int(row["xmax"] - row["xmin"])
			new_height = int(row["ymax"] - row["ymin"])
			x_coord, y_coord = (int(row["xmin"]), int(row["ymin"]))
			if not (
				x_coord < -new_width or y_coord < -new_height or x_coord > base_image.width or
				y_coord > base_image.height
			):
				crop_index = row["source_index"] % len(tree_crops)
				resized_crop = tree_crops[crop_index].resize((new_width, new_height))
				# corrected box to paste crop in
				dest_xmin = 0 if x_coord < 0 else x_coord
				dest_ymin = 0 if y_coord < 0 else y_coord
				dest_xmax = base_image.width if x_coord + new_width > base_image.width else x_coord + new_width
				dest_ymax = base_image.height if y_coord + new_height > base_image.height else y_coord + new_height
				corrected_width = dest_xmax - dest_xmin
				corrected_height = dest_ymax - dest_ymin
				# corrected rectangle to take from source crop
				source_xmin = dest_xmin - x_coord
				source_ymin = dest_ymin - y_coord
				source_xmax = source_xmin + corrected_width
				source_ymax = source_ymin + corrected_height
				resized_crop = resized_crop.crop(
					box=(source_xmin, source_ymin, source_xmax, source_ymax)
				)
				source_image.alpha_composite(resized_crop, dest=(dest_xmin, dest_ymin))
		return source_image

	@staticmethod
	def render_trees(base_image: Image, trees: DataFrame, scaling: int = 1):
		"""
		Renders trees on top of a base image based on new trees in a dataframe.
		Other trees on the base image are used to render these new trees.
		:param base_image: The image to render the trees onto
		:param trees: A dataframe containing all the trees
		:param scaling: A scaling factor for varying the resolution of the rendered image.
		:return: The resulting image
		"""
		source_trees = trees.loc[trees['label'] == "Tree"]
		trees_to_add = trees.loc[trees['label'] != "Tree"]
		source_image = base_image.copy()
		for (_, row) in trees_to_add.iterrows():
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
