"""
See :class:`.ScenarioRenderer`
"""
import pandas as pd
import numpy as np
import copy
import math
import cv2
from PIL import Image, ImageDraw, ImageOps

from mesh_city.gui.request_renderer import RequestRenderer
from mesh_city.request.entities.request import Request
from mesh_city.request.layers.google_layer import GoogleLayer
from mesh_city.scenario.scenario import Scenario
from mesh_city.util.image_util import ImageUtil


class ScenarioRenderer:
	"""
	A class used to create scenario's from requests whose behaviour can be customized by specifying
	what type of things it should change.
	"""

	def render_scenario(self, scenario: Scenario, request: Request,
	                    scaling: int = 1):
		"""
		Composites a rendering of a scenario
		:param scenario: The scenario to render
		:param request: The request the scenario is based of
		:param scaling: A scaling factor for low-resolution rendering
		:return: An image representation of the layer.
		"""
		tiles = request.get_layer_of_type(GoogleLayer).tiles
		images = []
		for tile in tiles:
			large_image = Image.open(tile.path).convert("RGBA")
			width, height = large_image.size
			images.append(large_image.resize((round(width / scaling), round(height / scaling))))
		base_image = ImageUtil.concat_image_grid(
			width=request.num_of_horizontal_images,
			height=request.num_of_vertical_images,
			images=images
		).convert("RGBA")

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

	def paint_buildings_green(self):
		# composes an image based on the new dataframe
		green_overlay_img = Image.open(str(self.overlay_path)).convert("RGB")
		green_overlay = np.asarray(green_overlay_img)
		vertical_tiles = math.ceil(self.base_image.width / green_overlay_img.height)
		horizontal_tiles = math.ceil(self.base_image.height / green_overlay_img.width)
		tiled_overlay = np.tile(green_overlay, (vertical_tiles, horizontal_tiles, 1))
		cropped_overlay = tiled_overlay[0:self.base_image.width, 0:self.base_image.height]
		mask_base = Image.new(
			'RGB',
			(
				self.base_image.width,
				self.base_image.height
			), (0, 0, 0)
		)
		draw = ImageDraw.Draw(mask_base)
		for (index, (polygon, label)) in enumerate(
			zip(final_dataframe["geometry"], final_dataframe["label"])):
			if label == "Shrubbery":
				vertices = list(zip(*polygon.exterior.coords.xy))
				draw.polygon(
					xy=vertices, fill=(255, 255, 255)
				)
		final_mask = np.asarray(mask_base).astype(float) / 255
		final_overlay = cv2.multiply(final_mask, cropped_overlay, dtype=cv2.CV_32F)
		masked_numpy_base = cv2.multiply(1 - final_mask, np.asarray(self.base_image.convert("RGB")),
		                                 dtype=cv2.CV_32F)
		new_base_image_numpy = cv2.add(masked_numpy_base, final_overlay, dtype=cv2.CV_8UC3)
		self.base_image = Image.fromarray(new_base_image_numpy.astype(np.uint8)).convert("RGBA")
		temp_to_add_image = copy.deepcopy(self.base_image)
		self.images_to_add.append(temp_to_add_image)

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

	def combine_results(self, request: Request) -> Scenario:
		"""
		Combines the results of the made modifications that are part of the Scenario.
		:param request: The request
		:return: The resulting Scenario.
		"""

		self.notify_observers_combination()

		scenario_path = self.request_manager.get_image_root().joinpath("scenarios")
		scenario_path.mkdir(parents=True, exist_ok=True)

		scenario_name = "Scenario" + str(len(request.scenarios))
		if self.name is not None:
			scenario_name = self.name

		scenario_file_name = "request" + str(request.request_id) + "_" + scenario_name
		scenario_file_gif = scenario_file_name + "_.gif"
		scenario_file_path_gif = scenario_path.joinpath(scenario_file_gif)

		scenario_file_csv = scenario_file_name + "_.csv"
		scenario_file_path_csv = scenario_path.joinpath(scenario_file_csv)

		scenario_file_png = scenario_file_name + "_.png"
		scenario_file_path_png = scenario_path.joinpath(scenario_file_png)

		self.images_to_add[len(self.images_to_add) - 1].save(fp=scenario_file_path_png)

		self.images_to_add[0].save(
			fp=scenario_file_path_gif,
			save_all=True,
			append_images=self.images_to_add[1:],
			optimize=False,
			duration=100,
			loop=0
		)

		self.changes_pd.to_csv(path_or_buf=scenario_file_path_csv)

		return Scenario(
			scenario_name=scenario_name,
			width=request.num_of_horizontal_images,
			height=request.num_of_vertical_images,
			scenario_path=scenario_file_path_gif,
			information_path=scenario_file_path_csv,
			picture_path=scenario_file_path_png
		)

	def process(self, request: Request, scaling=16) -> Scenario:
		"""
		Processes a request that is assumed to have a GoogleLayer with imagery (errors otherwise) and
		returns a list of detection layers corresponding to the detections_to_run variable.

		:param request: The request to process. Must have a GoogleLayer
		:return:
		"""

		if not request.has_layer_of_type(GoogleLayer):
			raise ValueError(
				"The request to process should have imagery to create scenarios based of"
			)

		self.base_image = RequestRenderer.create_image_from_layer(
			request=request, layer_index=0, scaling=scaling
		)
		self.images_to_add = []
		self.images_to_add.append(self.base_image)

		self.changes_pd = pd.DataFrame(columns=["xmin", "ymin", "xmax", "ymax", "score", "label"])

		self.trees = None
		self.cars = None

		for (feature, information) in self.scenarios_to_create:
			if feature == ScenarioModificationType.MORE_TREES:
				self.add_more_trees(request=request, trees_to_add=information, scaling=scaling)
			if feature == ScenarioModificationType.SWAP_CARS:
				self.swap_cars_with_trees(request=request, cars_to_swap=information,
				                          scaling=scaling)
			if feature == ScenarioModificationType.PAINT_BUILDINGS_GREEN:
				self.paint_buildings_green(request=request, buildings_to_make_green=information,
				                           scaling=scaling)
		new_scenario = self.combine_results(request)

		return new_scenario

	def attach_observer(self, observer):
		"""
		Attaches a observer to the scenario pipeline
		:param observer: the observer to attach
		:return: nothing
		"""
		self.observers.append(observer)

	def detach_observer(self, observer):
		"""
		Detaches a observer from the scenario pipeline and gets rid of its gui
		:param observer: the observer to detach
		:return:
		"""
		observer.destroy()
		self.observers.remove(observer)

	def notify_observers(self):
		"""
		Notifies all observers about a change in the state of the scenario pipeline
		:return:
		"""
		for observer in self.observers:
			observer.update(self)

	def notify_observers_combination(self):
		"""
		Notifies all observers that the images are being combined right now
		:return:
		"""
		for observer in self.observers:
			observer.update_combination()
