"""
See :class:`.ScenarioPipeline`

source for the part of creating an elipse mask for the trees:
source: Nadia Alramli
url: https://stackoverflow.com/questions/890051/how-do-i-generate-circular-thumbnails-with-pil
"""

import copy
import math
import random
from enum import Enum
from pathlib import Path
from typing import Any, Sequence, Tuple

import cv2
import geopandas as gpd
import numpy as np
import pandas as pd
from pandas import DataFrame
from PIL import Image, ImageDraw, ImageOps

from mesh_city.gui.request_renderer import RequestRenderer
from mesh_city.request.entities.request import Request
from mesh_city.request.layers.buildings_layer import BuildingsLayer
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
		overlay_path: Path,
		name: str = None
	):
		self.overlay_path = overlay_path
		self.request_manager = request_manager
		self.scenarios_to_create = scenarios_to_create
		self.name = name
		self.base_image = None
		self.images_to_add = None
		self.observers = []
		self.state = {}

	def paint_buildings_green(self, building_dataframe, buildings_to_make_green: int,
	                          scaling: int = 1):
		# to make shuffling deterministic for now

		# changes buildings to shrubbery patches in the dataframe
		np.random.shuffle(building_dataframe.values)
		shrubbery_dataframe = building_dataframe.head(buildings_to_make_green)
		shrubbery_dataframe["label"] = "Shrubbery"
		new_building_dataframe = building_dataframe.iloc[buildings_to_make_green:]
		final_dataframe = shrubbery_dataframe.append(new_building_dataframe, ignore_index=True)
		return final_dataframe

	def add_more_trees(self, tree_dataframe, trees_to_add: int, scaling: int = 1):
		"""
		Adds more trees to the image based on the detected trees
		:param request: the request for which to add more trees to
		:param trees_to_add: how many trees to add
		:return:
		"""
		# pylint: disable=W0612
		self.state["scenario_type"] = "Adding more trees"
		self.state["total_frames"] = trees_to_add
		self.state["current_frame"] = 1
		self.notify_observers()
		new_trees = []
		for tree_index in range(0, trees_to_add):
			source_tree_index = np.random.randint(1, len(tree_dataframe) - 1)
			neighbour_tree_index = np.random.randint(1, len(tree_dataframe) - 1)
			new_xmin, new_ymin, new_xmax, new_ymax = self.calculate_new_location_tree_addition(
				source_tree_index, neighbour_tree_index, tree_dataframe
				)
			new_trees.append(
				(new_xmin, new_ymin, new_xmax, new_ymax, tree_dataframe.loc[source_tree_index,["score"]],"AddedTree"))

		new_trees_df = pd.DataFrame(new_trees,columns =["xmin", "ymin", "xmax", "ymax", "score", "label"])
		tree_dataframe = tree_dataframe.append(new_trees_df,ignore_index=True)
		print(tree_dataframe)
		return tree_dataframe

	def swap_cars_with_trees(self, car_dataframe, tree_dataframe, cars_to_swap: int,
	                         scaling: int = 1):
		"""

		:param request:
		:param cars_to_swap:
		:return:
		"""
		self.state["scenario_type"] = "Swapping cars with trees"
		self.state["total_frames"] = cars_to_swap
		self.state["current_frame"] = 1
		self.notify_observers()
		np.random.seed(42)
		np.random.shuffle(car_dataframe.values)
		changes_list = []
		for car_index in range(0, cars_to_swap):
			tree_to_replace_with_index = np.random.randint(1, len(tree_dataframe) - 1)
			new_xmin, new_ymin, new_xmax, new_ymax = self.create_new_swapped_tree_entry(
				car_index, tree_to_replace_with_index, tree_dataframe, car_dataframe
			)
			changes_list.append(
				(new_xmin, new_ymin, new_xmax, new_ymax, tree_to_replace_with_index))
		replaced_cars = car_dataframe.head(cars_to_swap)
		tree_dataframe.loc[:, "source_index"] = -1
		replaced_cars.loc[:, "source_index"] = -1
		replaced_cars.loc[:, ["xmin", "ymin", "xmax", "ymax", "source_index"]] = changes_list
		replaced_cars.loc[:, "label"] = "SwappedCar"
		car_dataframe = car_dataframe[cars_to_swap:]
		tree_dataframe = tree_dataframe.append(replaced_cars, ignore_index=True)
		return tree_dataframe, car_dataframe

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
		tree_xmin = tree_dataframe.iloc[tree_to_replace_with_index][0]
		tree_ymin = tree_dataframe.iloc[tree_to_replace_with_index][1]
		tree_xmax = tree_dataframe.iloc[tree_to_replace_with_index][2]
		tree_ymax = tree_dataframe.iloc[tree_to_replace_with_index][3]

		tree_distance_center_max_x = (tree_xmax - tree_xmin) / 2
		tree_distance_center_max_y = (tree_ymax - tree_ymin) / 2

		car_xmin = car_dataframe.iloc[car_to_swap_index][0]
		car_ymin = car_dataframe.iloc[car_to_swap_index][1]
		car_xmax = car_dataframe.iloc[car_to_swap_index][2]
		car_ymax = car_dataframe.iloc[car_to_swap_index][3]

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

		return new_xmin, new_ymin, new_xmax, new_ymax,

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

		where_xmin = tree_dataframe.iloc[where_to_place][1]
		where_ymin = tree_dataframe.iloc[where_to_place][2]
		where_xmax = tree_dataframe.iloc[where_to_place][3]
		where_ymax = tree_dataframe.iloc[where_to_place][4]

		where_center_x = where_xmin + ((where_xmax - where_xmin) / 2)
		where_center_y = where_ymin + ((where_ymax - where_ymin) / 2)

		y_offset = random.uniform(-50, 50)
		x_offset = random.uniform(-50, 50)

		new_center_y = where_center_y + y_offset
		new_center_x = where_center_x + x_offset

		new_xmin = new_center_x + ((old_xmax - old_xmin) / 2)
		new_xmax = new_center_x + ((old_xmax - old_xmin) / 2)
		new_ymin = new_center_y + ((old_ymax - old_ymin) / 2)
		new_ymax = new_center_y + ((old_ymax - old_ymin) / 2)

		if new_xmin < 0:
			to_add = (-1) * new_xmin
			new_xmin = new_xmin + to_add
			new_xmax = new_xmax + to_add

		if new_ymin < 0:
			to_add = (-1) * new_ymin
			new_ymin = new_ymin + to_add
			new_ymax = new_ymax + to_add

		return new_xmin, new_ymin, new_xmax, new_ymax

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
		car_dataframe = None
		tree_dataframe = None
		buildings_dataframe = None
		if request.has_layer_of_type(CarsLayer):
			car_dataframe = pd.read_csv(request.get_layer_of_type(CarsLayer).detections_path,
			                            index_col=0)
		if request.has_layer_of_type(TreesLayer):
			tree_dataframe = pd.read_csv(request.get_layer_of_type(TreesLayer).detections_path,
			                             index_col=0)
		if request.has_layer_of_type(BuildingsLayer):
			buildings_dataframe = gpd.read_file(
				request.get_layer_of_type(BuildingsLayer).detections_path)

		for (feature, information) in self.scenarios_to_create:
			if feature == ScenarioModificationType.MORE_TREES:
				tree_dataframe = self.add_more_trees(tree_dataframe=tree_dataframe,
				                                     trees_to_add=information, scaling=scaling)
			if feature == ScenarioModificationType.SWAP_CARS:
				tree_dataframe, car_dataframe = self.swap_cars_with_trees(
					car_dataframe=car_dataframe, tree_dataframe=tree_dataframe,
					cars_to_swap=information,
					scaling=scaling)
			if feature == ScenarioModificationType.PAINT_BUILDINGS_GREEN:
				buildings_dataframe = self.paint_buildings_green(
					building_dataframe=buildings_dataframe, buildings_to_make_green=information,
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
