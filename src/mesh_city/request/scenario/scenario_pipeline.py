import copy
import random
from enum import Enum
from typing import Sequence

import pandas as pd

from mesh_city.gui.request_renderer import RequestRenderer
from mesh_city.request.entities.request import Request
from mesh_city.request.layers.google_layer import GoogleLayer
from mesh_city.request.layers.trees_layer import TreesLayer
from mesh_city.request.request_manager import RequestManager
from mesh_city.request.scenario.more_trees_scenario import MoreTreesScenario
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

		tree_layer_panda = pd.read_csv(request.get_layer_of_type(TreesLayer).detections_path)

		temp_image = RequestRenderer.create_image_from_layer(
			request=request, layer_index=0, scaling=1
		)

		images_to_add = []
		images_to_add.append(temp_image)
		object_counter = tree_layer_panda.shape[0] - 1

		# pylint: disable=W0612
		for tree in range(0, trees_to_add):
			tree_to_duplicate = random.randint(1, tree_layer_panda.shape[0] - 1)
			location_to_place_it_to = random.randint(1, tree_layer_panda.shape[0] - 1)
			image_to_paste = temp_image.crop(
				box=(
				float(tree_layer_panda.iloc[tree_to_duplicate][1]),  #xmin
				float(tree_layer_panda.iloc[tree_to_duplicate][2]),  #ymin
				float(tree_layer_panda.iloc[tree_to_duplicate][3]),  #xmax
				float(tree_layer_panda.iloc[tree_to_duplicate][4]),  #ymax
				)
			)

			new_entry = self.calculate_new_location(
				tree_to_duplicate, location_to_place_it_to, tree_layer_panda
			)
			tree_layer_panda.loc[object_counter] = new_entry
			object_counter += 1

			where_to_place = ((int(float(new_entry[1])), int(float(new_entry[4]))))

			temp_image.paste(image_to_paste, box=where_to_place)
			temp_to_add_image = copy.deepcopy(temp_image)
			images_to_add.append(temp_to_add_image)

		more_trees_scenario_path = self.request_manager.get_image_root().joinpath("scenarios")
		more_trees_scenario_path.mkdir(parents=True, exist_ok=True)

		scenario_name = "MoreTrees" + str(len(request.scenarios))
		if self.name is not None:
			scenario_name = self.name

		more_trees_file_name = "request" + str(request.request_id) + "_" + scenario_name + "_.gif"
		more_trees_file_path = more_trees_scenario_path.joinpath(more_trees_file_name)

		images_to_add[0].save(
			fp=more_trees_file_path,
			save_all=True,
			append_images=images_to_add[1:],
			optimize=False,
			duration=100,
			loop=0
		)

		return MoreTreesScenario(
			scenario_name=scenario_name,
			width=request.num_of_horizontal_images,
			height=request.num_of_vertical_images,
			scenario_path=more_trees_file_path
		)

	# pylint: disable=W0613
	def calculate_new_location(self, what_to_place, where_to_place, tree_layer_panda):
		"""
		The algorithm to decide where to place a new tree. Currently just moves the tree 5 units
		down and to the right
		:param what_to_place: the tree to place
		:param where_to_place: the location adjacent to which to place it at
		:return: where to place the tree
		"""
		old_xmin = tree_layer_panda.iloc[what_to_place][1]
		old_ymax = tree_layer_panda.iloc[what_to_place][2]
		old_xmax = tree_layer_panda.iloc[what_to_place][3]
		old_ymin = tree_layer_panda.iloc[what_to_place][4]

		new_xmin = str(float(old_xmin) + 50)
		new_ymax = str(float(old_ymax) + 50)
		new_xmax = str(float(old_xmax) + 50)
		new_ymin = str(float(old_ymin) + 50)

		new_entry = [
			tree_layer_panda.shape[0],
			new_xmin,
			new_ymin,
			new_xmax,
			new_ymax,
			tree_layer_panda.iloc[what_to_place][5],
			"Tree"
		]

		return new_entry

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

		new_scenario = []
		for (feature, information) in self.scenarios_to_create:
			if feature == ScenarioType.MORE_TREES:
				new_scenario.append(self.add_more_trees(request=request, trees_to_add=information))

		# TODO fix so that it does not only return first scenario
		return new_scenario[0]
