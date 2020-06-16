import copy
import random
from enum import Enum
from typing import Sequence

import pandas as pd

from mesh_city.gui.request_renderer import RequestRenderer
from mesh_city.request.entities.request import Request
from mesh_city.request.layers.cars_layer import CarsLayer
from mesh_city.request.layers.google_layer import GoogleLayer
from mesh_city.request.layers.trees_layer import TreesLayer
from mesh_city.request.request_manager import RequestManager
from mesh_city.request.scenario.scenario import Scenario
from mesh_city.util.file_handler import FileHandler


class ScenarioType(Enum):

	MORE_TREES = 0
	SWAP_CARS = 1

class ScenarioPipeline:

	def __init__(
		self,
		file_handler: FileHandler,
		request_manager: RequestManager,
		scenarios_to_create,
		name=None
	):
		self.file_handler = file_handler
		self.scenarios_to_create = scenarios_to_create
		self.request_manager = request_manager
		self.name = name

	def add_more_trees(self, request, trees_to_add):

		if self.tree_panda is None:
			tree_dataframe = pd.read_csv(request.get_layer_of_type(TreesLayer).detections_path)
		else:
			tree_dataframe = self.tree_panda

		object_counter = tree_dataframe.shape[0] - 1

		# pylint: disable=W0612
		for tree in range(0, trees_to_add):
			source_tree_index = random.randint(1, tree_dataframe.shape[0])
			destination_tree_index = random.randint(1, tree_dataframe.shape[0])
			source_tree_image = self.base_image.crop(
				box=(
				float(tree_dataframe.iloc[source_tree_index][1]),  #xmin
				float(tree_dataframe.iloc[source_tree_index][2]),  #ymin
				float(tree_dataframe.iloc[source_tree_index][3]),  #xmax
				float(tree_dataframe.iloc[source_tree_index][4]),  #ymax
				)
			)

			new_entry = self.calculate_new_location_tree_addition(
				source_tree_index, destination_tree_index, tree_dataframe
			)
			tree_dataframe.loc[object_counter] = new_entry
			object_counter += 1

			new_entry[6] = "AddedTree"
			del new_entry[0]
			temp_index = len(self.changes_pd)
			self.changes_pd.loc[temp_index] = new_entry

			coordinate = ((int(float(new_entry[1])), int(float(new_entry[4]))))

			self.base_image.paste(source_tree_image, box=coordinate)
			temp_to_add_image = copy.deepcopy(self.base_image)
			self.images_to_add.append(temp_to_add_image)

		self.tree_panda = tree_dataframe

	def swap_cars_with_trees(self, request, cars_to_swap):

		if self.car_panda is None:
			car_dataframe = pd.read_csv(request.get_layer_of_type(CarsLayer).detections_path)
		else:
			car_dataframe = self.car_panda

		if self.tree_panda is None:
			tree_dataframe = pd.read_csv(request.get_layer_of_type(TreesLayer).detections_path)
		else:
			tree_dataframe = self.tree_panda

		object_counter = tree_dataframe.shape[0] - 1

		# pylint: disable=W0612
		for car in range(0, cars_to_swap):
			car_to_swap_index = random.randint(1, car_dataframe.shape[0])
			tree_to_replace_with_index = random.randint(1, car_dataframe.shape[0])

			tree_image = self.base_image.crop(
				box=(
				float(tree_dataframe.iloc[tree_to_replace_with_index][1]),  #xmin
				float(tree_dataframe.iloc[tree_to_replace_with_index][2]),  #ymin
				float(tree_dataframe.iloc[tree_to_replace_with_index][3]),  #xmax
				float(tree_dataframe.iloc[tree_to_replace_with_index][4]),  #ymax
				)
			)

			new_entry = self.calculate_car_swap_location(car_to_swap_index, tree_to_replace_with_index,
			                                             tree_dataframe, car_dataframe)
			tree_dataframe.loc[object_counter] = new_entry
			object_counter += 1

			new_entry[6] = "SwapedCar"
			self.changes_pd.append(new_entry)

			car_dataframe.drop(car_dataframe.index[car_to_swap_index])

			coordinate = ((int(float(new_entry[1])), int(float(new_entry[4]))))
			self.base_image.paste(tree_image, box=coordinate)

			temp_to_add_image = copy.deepcopy(self.base_image)
			self.images_to_add.append(temp_to_add_image)

		self.tree_panda = tree_dataframe
		self.car_panda = car_dataframe

	def calculate_car_swap_location(self, car_to_swap_index, tree_to_replace_with_index,
	                                tree_dataframe, car_dataframe):

		tree_xmin = tree_dataframe.iloc[tree_to_replace_with_index][1]
		tree_ymax = tree_dataframe.iloc[tree_to_replace_with_index][2]
		tree_xmax = tree_dataframe.iloc[tree_to_replace_with_index][3]
		tree_ymin = tree_dataframe.iloc[tree_to_replace_with_index][4]

		tree_distance_center_max_x = tree_xmax / 2
		tree_distance_center_max_y = tree_ymax / 2

		car_xmin = car_dataframe.iloc[car_to_swap_index][1]
		car_ymax = car_dataframe.iloc[car_to_swap_index][2]
		car_xmax = car_dataframe.iloc[car_to_swap_index][3]
		car_ymin = car_dataframe.iloc[car_to_swap_index][4]

		car_center_x = (car_xmax - car_xmin) / 2
		car_center_y = (car_ymax - car_ymin) / 2

		new_xmin = car_center_x - tree_distance_center_max_x
		new_xmax = car_center_x + tree_distance_center_max_x
		new_ymin = car_center_y - tree_distance_center_max_y
		new_ymax = car_center_y + tree_distance_center_max_y

		new_entry = [
			tree_dataframe.shape[0],
			new_xmin,
			new_ymin,
			new_xmax,
			new_ymax,
			tree_dataframe.iloc[tree_to_replace_with_index][5],
			"Tree"
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
		old_ymax = tree_dataframe.iloc[what_to_place][2]
		old_xmax = tree_dataframe.iloc[what_to_place][3]
		old_ymin = tree_dataframe.iloc[what_to_place][4]

		new_xmin = str(float(old_xmin) + 50)
		new_ymax = str(float(old_ymax) + 50)
		new_xmax = str(float(old_xmax) + 50)
		new_ymin = str(float(old_ymin) + 50)

		new_entry = [
			tree_dataframe.shape[0],
			new_xmin,
			new_ymin,
			new_xmax,
			new_ymax,
			tree_dataframe.iloc[what_to_place][5],
			"Tree"
		]

		return new_entry

	def combine_results(self, request):

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
			scenario_path=scenario_file_path_gif
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

		self.changes_pd = pd.DataFrame(columns=["xmin","ymin","xmax","ymax","score","label"])

		self.tree_panda = None
		self.car_panda = None

		for (feature, information) in self.scenarios_to_create:
			if feature == ScenarioType.MORE_TREES:
				self.add_more_trees(request=request, trees_to_add=information)
			if feature == ScenarioType.SWAP_CARS:
				self.swap_cars_with_trees(request=request, cars_to_swap=information)

		new_scenario = self.combine_results(request)

		return new_scenario
