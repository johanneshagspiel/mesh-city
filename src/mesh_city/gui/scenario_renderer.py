"""
See :class:`.ScenarioRenderer`
"""
import copy
import math

import cv2
import numpy as np
from pandas import DataFrame
from PIL import Image, ImageDraw, ImageOps

from mesh_city.request.entities.request import Request
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

	def render_scenario(self, scenario: Scenario, scaling: int = 1) -> Image:
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
		if scenario.buildings is not None:
			result_image = self.paint_buildings_green(base_image=result_image,buildings=scenario.buildings)
		return result_image

	def paint_buildings_green(self, base_image: Image, buildings: DataFrame) -> Image:
		# composes an image based on the new dataframe
		green_overlay = np.asarray(self.overlay_image)
		vertical_tiles = math.ceil(base_image.width / self.overlay_image.height)
		horizontal_tiles = math.ceil(base_image.height / self.overlay_image.width)
		tiled_overlay = np.tile(green_overlay, (vertical_tiles, horizontal_tiles, 1))
		cropped_overlay = tiled_overlay[0:base_image.width, 0:base_image.height]
		mask_base = Image.new(
			'RGB',
			(
				base_image.width,
				base_image.height
			), (0, 0, 0)
		)
		draw = ImageDraw.Draw(mask_base)
		for (index, (polygon, label)) in enumerate(
			zip(buildings["geometry"], buildings["label"])):
			if label == "Shrubbery":
				vertices = list(zip(*polygon.exterior.coords.xy))
				draw.polygon(
					xy=vertices, fill=(255, 255, 255)
				)
		final_mask = np.asarray(mask_base).astype(float) / 255
		final_overlay = cv2.multiply(final_mask, cropped_overlay, dtype=cv2.CV_32F)
		masked_numpy_base = cv2.multiply(1 - final_mask, np.asarray(base_image.convert("RGB")),
		                                 dtype=cv2.CV_32F)
		new_base_image_numpy = cv2.add(masked_numpy_base, final_overlay, dtype=cv2.CV_8UC3)
		return Image.fromarray(new_base_image_numpy.astype(np.uint8)).convert("RGBA")

	def add_more_trees(self, request: Request, trees_to_add: int, scaling: int = 1):
		"""
		Adds more trees to the image based on the detected trees
		:param request: the request for which to add more trees to
		:param trees_to_add: how many trees to add
		:return:
		"""
		for tree in range(0, trees_to_add):
			source_tree_index = random.randint(1, len(tree_dataframe) - 1)
			destination_tree_index = random.randint(1, len(tree_dataframe) - 1)

			tree_area_to_cut = (
				float(tree_dataframe.iloc[source_tree_index][1]) / scaling,  # xmin
				float(tree_dataframe.iloc[source_tree_index][2]) / scaling,  # ymin
				float(tree_dataframe.iloc[source_tree_index][3]) / scaling,  # xmax
				float(tree_dataframe.iloc[source_tree_index][4]) / scaling,  # ymax
			)

			tree_image_cropped = self.base_image.crop(box=tree_area_to_cut)

			mask = Image.new('L', tree_image_cropped.size, 0)
			draw = ImageDraw.Draw(mask)
			draw.ellipse((0, 0) + tree_image_cropped.size, fill=255)

			source_tree_image = ImageOps.fit(tree_image_cropped, mask.size, centering=(0.5, 0.5))
			source_tree_image.putalpha(mask)

			new_entry = self.calculate_new_location_tree_addition(
				source_tree_index, destination_tree_index, tree_dataframe
			)

			temp_index = len(self.changes_pd)
			self.changes_pd.loc[temp_index] = new_entry

			coordinate = ((int(new_entry[0] / scaling), int(new_entry[3] / scaling)))

			self.base_image.alpha_composite(source_tree_image, dest=coordinate)
			temp_to_add_image = copy.deepcopy(self.base_image)
			self.images_to_add.append(temp_to_add_image)

			self.state["current_frame"] = tree + 1
			self.notify_observers()

	def swap_cars_with_trees(self, request: Request, cars_to_swap: int, scaling: int = 1):
		"""
		Modifies the
		:param request:
		:param cars_to_swap:
		:return:
		"""
		for index, row in replaced_cars.iterrows():
			tree_xmin = int(tree_dataframe.loc[row['source_index'], ["xmin"]] / scaling)
			tree_ymin = int(tree_dataframe.loc[row['source_index'], ["ymin"]] / scaling)
			tree_xmax = int(tree_dataframe.loc[row['source_index'], ["xmax"]] / scaling)
			tree_ymax = int(tree_dataframe.loc[row['source_index'], ["ymax"]] / scaling)

			tree_area_to_cut = (tree_xmin, tree_ymin, tree_xmax, tree_ymax)

			tree_image_cropped = self.base_image.crop(box=tree_area_to_cut)

			mask = Image.new('L', tree_image_cropped.size, 0)
			draw = ImageDraw.Draw(mask)
			draw.ellipse((0, 0) + tree_image_cropped.size, fill=255)

			tree_image = ImageOps.fit(tree_image_cropped, mask.size, centering=(0.5, 0.5))
			tree_image.putalpha(mask)

			coordinate = ((int(row["xmin"] / scaling), int(row["ymin"] / scaling)))
			self.base_image.alpha_composite(tree_image, dest=coordinate)

			temp_to_add_image = copy.deepcopy(self.base_image)
			self.images_to_add.append(temp_to_add_image)

			self.state["current_frame"] = index + 1
			self.notify_observers()
