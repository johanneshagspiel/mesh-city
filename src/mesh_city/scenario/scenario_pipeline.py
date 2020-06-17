"""
See :class:`.ScenarioPipeline`

source for the part of creating an elipse mask for the trees:
source: Nadia Alramli
url: https://stackoverflow.com/questions/890051/how-do-i-generate-circular-thumbnails-with-pil
"""

import copy
import random
from enum import Enum
from typing import Any, Sequence, Tuple

import pandas as pd
from pandas import DataFrame
from PIL import Image, ImageDraw, ImageOps

from mesh_city.gui.request_renderer import RequestRenderer
from mesh_city.request.entities.request import Request
from mesh_city.request.layers.cars_layer import CarsLayer
from mesh_city.request.layers.google_layer import GoogleLayer
from mesh_city.request.layers.trees_layer import TreesLayer
from mesh_city.request.request_manager import RequestManager
from mesh_city.scenario.scenario import Scenario


class ScenarioModificationType(Enum):
	"""
	Enum class representing types of modifications that can be part of a scenario.
	"""
	MORE_TREES = 0
	SWAP_CARS = 1
	PAINT_BUILDINGS_GREEN = 2

class ScenarioPipeline:
	"""
	A class used to create scenario's from requests whose behaviour can be customized by specifying
	what type of things it should change.
	"""

	def __init__(
		self,
		request_manager: RequestManager,
		scenarios_to_create: Sequence[Tuple[ScenarioModificationType, Any]],
		name: str = None
	):
		self.request_manager = request_manager
		self.scenarios_to_create = scenarios_to_create
		self.name = name
		self.trees = None
		self.cars = None
		self.base_image = None
		self.images_to_add = None
		self.changes_pd = None
		self.observers= []
		self.state = {}

	def paint_buildings_green(self, request: Request, buildings_to_make_green: int):
		pass


	def add_more_trees(self, request: Request, trees_to_add: int):
		"""
		Creates the dataframes nee
		:param request:
		:param trees_to_add:
		:return:
		"""
		if self.trees is None:
			tree_dataframe = pd.read_csv(request.get_layer_of_type(TreesLayer).detections_path)
		else:
			tree_dataframe = self.trees


		# pylint: disable=W0612
		self.state["scenario_type"] = "Adding more trees"
		self.state["total_frames"] = trees_to_add
		self.state["current_frame"] = 1
		self.notify_observers()

		for tree in range(0, trees_to_add):
			source_tree_index = random.randint(1, tree_dataframe.shape[0] - 1)
			destination_tree_index = random.randint(1, tree_dataframe.shape[0] - 1)


			tree_area_to_cut=(
				float(tree_dataframe.iloc[source_tree_index][1]),  # xmin
				float(tree_dataframe.iloc[source_tree_index][2]),  # ymin
				float(tree_dataframe.iloc[source_tree_index][3]),  # xmax
				float(tree_dataframe.iloc[source_tree_index][4]),  # ymax
				)

			tree_image_cropped = self.base_image.crop(
				box=tree_area_to_cut
			)

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

			coordinate = ((int(new_entry[0]), int(new_entry[3])))

			self.base_image.alpha_composite(source_tree_image, dest=coordinate)
			temp_to_add_image = copy.deepcopy(self.base_image)
			self.images_to_add.append(temp_to_add_image)

			self.state["current_frame"] = tree + 1
			self.notify_observers()

		self.trees = tree_dataframe

	def swap_cars_with_trees(self, request: Request, cars_to_swap: int):
		"""
		Modifies the
		:param request:
		:param cars_to_swap:
		:return:
		"""

		if self.cars is None:
			car_dataframe = pd.read_csv(request.get_layer_of_type(CarsLayer).detections_path)
		else:
			car_dataframe = self.cars

		if self.trees is None:
			tree_dataframe = pd.read_csv(request.get_layer_of_type(TreesLayer).detections_path)
		else:
			tree_dataframe = self.trees

		self.state["scenario_type"] = "Swapping cars with trees"
		self.state["total_frames"] = cars_to_swap
		self.state["current_frame"] = 1
		self.notify_observers()

		# pylint: disable=W0612
		for car in range(0, cars_to_swap):
			car_to_swap_index_temp = random.randint(1, len(car_dataframe) - 1)
			car_to_swap_axis_name = car_dataframe.iloc[car_to_swap_index_temp][0]
			tree_to_replace_with_index = random.randint(1, len(tree_dataframe) - 1)

			tree_area_to_cut = (
				tree_dataframe.iloc[tree_to_replace_with_index][1],  # xmin
				tree_dataframe.iloc[tree_to_replace_with_index][2],  # ymin
				tree_dataframe.iloc[tree_to_replace_with_index][3],  # xmax
				tree_dataframe.iloc[tree_to_replace_with_index][4],  # ymax
				)

			tree_image_cropped = self.base_image.crop(
				box=tree_area_to_cut
			)

			mask = Image.new('L', tree_image_cropped.size, 0)
			draw = ImageDraw.Draw(mask)
			draw.ellipse((0, 0) + tree_image_cropped.size, fill=255)

			tree_image = ImageOps.fit(tree_image_cropped, mask.size, centering=(0.5, 0.5))
			tree_image.putalpha(mask)

			new_entry = self.create_new_swapped_tree_entry(
				car_to_swap_index_temp, tree_to_replace_with_index, tree_dataframe, car_dataframe
			)

			temp_index = len(self.changes_pd)
			self.changes_pd.loc[temp_index] = new_entry

			temp = car_dataframe.drop(car_to_swap_axis_name)
			car_dataframe = temp

			coordinate = ((int(new_entry[0]), int(new_entry[3])))
			self.base_image.alpha_composite(tree_image, dest=coordinate)

			temp_to_add_image = copy.deepcopy(self.base_image)
			self.images_to_add.append(temp_to_add_image)

			self.state["current_frame"] = car + 1
			self.notify_observers()

		self.trees = tree_dataframe
		self.cars = car_dataframe

	def create_new_swapped_tree_entry(
		self,
		car_to_swap_index: int,
		tree_to_replace_with_index: int,
		tree_dataframe: DataFrame,
		car_dataframe: DataFrame
	):
		"""
		Computes a new entry for a tree copied to where there is currently a car.
		:param car_to_swap_index: The car to paste a tree on
		:param tree_to_replace_with_index: The tree to paste onto the car
		:param tree_dataframe: The dataframe of tree detections
		:param car_dataframe: The dataframe of car detections
		:return: A new entry containing a tree copied to where the car was
		"""
		tree_xmin = tree_dataframe.iloc[tree_to_replace_with_index][1]
		tree_ymin = tree_dataframe.iloc[tree_to_replace_with_index][2]
		tree_xmax = tree_dataframe.iloc[tree_to_replace_with_index][3]
		tree_ymax = tree_dataframe.iloc[tree_to_replace_with_index][4]

		tree_distance_center_max_x = (tree_xmax - tree_xmin) / 2
		tree_distance_center_max_y = (tree_ymax - tree_ymin) / 2

		car_xmin = car_dataframe.iloc[car_to_swap_index][1]
		car_ymin = car_dataframe.iloc[car_to_swap_index][2]
		car_xmax = car_dataframe.iloc[car_to_swap_index][3]
		car_ymax = car_dataframe.iloc[car_to_swap_index][4]

		car_center_x = car_xmin + ((car_xmax - car_xmin) / 2)
		car_center_y = car_ymin + ((car_ymax - car_ymin) / 2)

		new_xmin = car_center_x - tree_distance_center_max_x
		new_xmax = car_center_x + tree_distance_center_max_x
		new_ymin = car_center_y - tree_distance_center_max_y
		new_ymax = car_center_y + tree_distance_center_max_y

		if new_xmin < 0:
			to_add = (-1) * new_xmin
			new_xmin = new_xmin + to_add
			new_xmax = new_xmax + to_add

		if new_ymin < 0:
			to_add = (-1) * new_ymin
			new_ymin = new_ymin + to_add
			new_ymax = new_ymax + to_add

		new_entry = [
			new_xmin,
			new_ymin,
			new_xmax,
			new_ymax,
			tree_dataframe.iloc[tree_to_replace_with_index][5],
			"SwappedCar"
		]

		return new_entry

	# pylint: disable=W0613
	def calculate_new_location_tree_addition(self, what_to_place, where_to_place, tree_dataframe):
		"""
		The algorithm to decide where to place a new tree. Currently just moves the tree 5 units
		down and to the right
		:param what_to_place: the tree to place
		:param where_to_place: the location adjacent to which to place it at
		:return: where to place the tree
		"""
		old_xmin = tree_dataframe.iloc[what_to_place][1]
		old_ymin = tree_dataframe.iloc[what_to_place][2]
		old_xmax = tree_dataframe.iloc[what_to_place][3]
		old_ymax = tree_dataframe.iloc[what_to_place][4]

		new_xmin = old_xmin + 50
		new_ymax = old_ymax + 50
		new_xmax = old_xmax + 50
		new_ymin = old_ymin + 50

		if new_xmin < 0:
			to_add = (-1) * new_xmin
			new_xmin = new_xmin + to_add
			new_xmax = new_xmax + to_add

		if new_ymin < 0:
			to_add = (-1) * new_ymin
			new_ymin = new_ymin + to_add
			new_ymax = new_ymax + to_add

		new_entry = [
			new_xmin,
			new_ymin,
			new_xmax,
			new_ymax,
			tree_dataframe.iloc[what_to_place][5],
			"AddedTree"
		]

		return new_entry

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

		self.images_to_add[len(self.images_to_add)-1].save(fp=scenario_file_path_png)

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

	def process(self, request: Request) -> Scenario:
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
			request=request, layer_index=0, scaling=1
		)
		self.images_to_add = []
		self.images_to_add.append(self.base_image)

		self.changes_pd = pd.DataFrame(columns=["xmin", "ymin", "xmax", "ymax", "score", "label"])

		self.trees = None
		self.cars = None

		for (feature, information) in self.scenarios_to_create:
			if feature == ScenarioModificationType.MORE_TREES:
				self.add_more_trees(request=request, trees_to_add=information)
			if feature == ScenarioModificationType.SWAP_CARS:
				self.swap_cars_with_trees(request=request, cars_to_swap=information)

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
