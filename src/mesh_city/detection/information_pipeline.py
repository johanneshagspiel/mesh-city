"""
See class description
"""
import csv
from pathlib import Path
from typing import Sequence, Union

from mesh_city.request.entities.request import Request
from mesh_city.request.layers.cars_layer import CarsLayer
from mesh_city.request.layers.layer import Layer
from mesh_city.request.layers.trees_layer import TreesLayer
from mesh_city.request.scenario.scenario import Scenario
from mesh_city.util.geo_location_util import GeoLocationUtil


class InformationStringBuilder:
	"""
	Class which contains methods to count, analyse and create some statistics of the detections
	saved in layers of a request.
	"""

	def __init__(self, bio_path: Path, request: Request):
		self.bio_path = bio_path
		self.request = request

	def get_tree_and_rooftop_co2_values(self):
		"""
		Analyses the biome information csv and the coordinates of the current request
		:return: the relevant biome values of the closest point in the list
		"""
		request = self.request

		info = []
		with open(str(self.bio_path), newline='') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for (index, row) in enumerate(csv_reader):
				if len(row) > 0 and index > 0:

					eco_name = row[1]
					longitude, latitude = row[2], row[3]
					carbon_storage = float(row[5].replace(',', '.'))
					temperature_delta = float(row[6].replace(',', '.'))

					latitude = latitude.replace(',', '.', 1)
					latitude = latitude.replace(',', '')
					latitude = float(latitude)

					longitude = longitude.replace(',', '.', 1)
					longitude = longitude.replace(',', '')
					longitude = float(longitude)

					dictionary = {
						'biodome': eco_name,
						'latitude': latitude,
						'longitude': longitude,
						'carbon_storage': carbon_storage,
						'temperature_delta': temperature_delta
					}
					info.append(dictionary)

		latitude, longitude = GeoLocationUtil.tile_value_to_degree(request.x_grid_coord,
						request.y_grid_coord, 20)
		point = {'latitude': latitude, 'longitude': longitude}

		closest = GeoLocationUtil.closest(info, point)

		print(latitude, longitude)
		print('closest', closest)

		return closest

	def process_tree_layer(self, tree_layer: TreesLayer) -> str:
		"""
		Generates information for a TreesLayer
		:param tree_layer: The TreesLayer to generate information for
		:return: An information string about the TreesLayer
		"""
		count = 0
		with open(str(tree_layer.detections_path), newline='') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for (index, row) in enumerate(csv_reader):
				if len(row) > 0 and index > 0:
					count += 1
		return "Trees Detected: " + str(count) + "\n"

	def process_cars_layer(self, cars_layer: CarsLayer) -> str:
		"""
		Generates information for a CarsLayer
		:param cars_layer: The CarsLayer to generate information for
		:return: An information string about the CarsLayer
		"""
		count = 0
		with open(str(cars_layer.detections_path), newline='') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for (index, row) in enumerate(csv_reader):
				if len(row) > 0 and index > 0:
					count += 1
		return "Cars Detected: " + str(count) + "\n"

	def process_scenario(self, scenario: Scenario) -> str:
		"""
		Process a given scenario by turning it into an informative string.
		:param scenario: A Scenario instance
		:return: An informative string about this Scenario
		"""
		count_trees_added = 0
		count_cars_swapped = 0

		with open(str(scenario.information_path), newline='') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for (index, row) in enumerate(csv_reader):
				if len(row) > 0 and index > 0:
					if row[6] == "AddedTree":
						count_trees_added += 1
					if row[6] == "SwappedCar":
						count_cars_swapped += 1
		result_string = ""
		if count_trees_added > 0:
			result_string += "Trees added: " + str(count_trees_added) + "\n"
		if count_cars_swapped > 0:
			result_string += "Cars swap with trees: " + str(count_cars_swapped) + "\n"
		return result_string

	def process(self, element_list: Sequence[Union[Layer, Scenario]]) -> str:
		"""
		Processes a list of elements that can be either Layers or Scenarios
		:param element_list: The list of Layers and/or Scenarios
		:return: The information string
		"""
		result_string = ""
		for element in element_list:
			if isinstance(element, TreesLayer):
				result_string += self.process_tree_layer(tree_layer=element)
			if isinstance(element, CarsLayer):
				result_string += self.process_cars_layer(cars_layer=element)
			if isinstance(element, Scenario):
				result_string += self.process_scenario(scenario=element)

		return result_string
