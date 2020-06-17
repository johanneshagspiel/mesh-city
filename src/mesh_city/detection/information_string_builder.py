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
from mesh_city.scenario.scenario import Scenario
from mesh_city.util.geo_location_util import GeoLocationUtil


class InformationStringBuilder:
	"""
	Class which contains methods to count, analyse and create some statistics of the detections
	saved in layers of a request.
	"""

	def __init__(self, bio_path: Path, request: Request):
		self.bio_path = bio_path
		self.request = request

	def get_tree_and_rooftop_co2_values(self, request: Request) -> dict:
		"""
		Analyses the biome information csv and the coordinates of the current request so that it
		returns the point in the PlanetPainter_BiomIndex.csv file, closest to the coordinates of the
		request
		:param request: The Request to create the information dictionary for.
		:return: a dictionary with the following fields with info:
		'biodome': eco_name,
		'latitude': latitude,
		'longitude': longitude,
		'carbon_storage': carbon_storage,
		'temperature_delta': temperature_delta
		"""

		info = []
		with open(str(self.bio_path), newline='') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for (index, row) in enumerate(csv_reader):
				if len(row) > 0 and index > 0:

					eco_name = row[1]
					longitude, latitude = row[2], row[3]
					carbon_storage_tree = float(row[5].replace(',', '.'))
					carbon_storage_rooftops = float(row[6].replace(',', '.'))
					oxygen_emission_tree = float(row[7].replace(',', '.'))
					oxygen_emission_rooftop = float(row[8].replace(',', '.'))
					carbon_emission_car = float(row[9].replace(',', '.'))
					urban_cooling_tree = float(row[10].replace(',', '.'))
					urban_cooling_rooftop = float(row[11].replace(',', '.'))

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
						'carbon_storage_tree': carbon_storage_tree,
						'carbon_storage_rooftops': carbon_storage_rooftops,
						'oxygen_emission_tree': oxygen_emission_tree,
						'oxygen_emission_rooftop': oxygen_emission_rooftop,
						'carbon_emission_car': carbon_emission_car,
						'urban_cooling_tree': urban_cooling_tree,
						'urban_cooling_rooftop': urban_cooling_rooftop
					}
					info.append(dictionary)

		latitude, longitude = GeoLocationUtil.tile_value_to_degree(request.x_grid_coord,
			request.y_grid_coord, 20)
		point = {'latitude': latitude, 'longitude': longitude}

		closest = GeoLocationUtil.closest(info, point)

		print(latitude, longitude)
		print('closest', closest)

		return closest

	def process_tree_layer(self, tree_layer: TreesLayer) -> int:
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
		return count

	def process_cars_layer(self, cars_layer: CarsLayer) -> int:
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
		return count

	def process_scenario(self, scenario: Scenario) -> (int, int):
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
		return count_trees_added, count_cars_swapped

	def process(self, element_list: Sequence[Union[Layer, Scenario]]) -> str:
		"""
		Processes a list of elements that can be either Layers or Scenarios
		:param element_list: The list of Layers and/or Scenarios
		:return: The information string
		"""
		info_dict = self.get_tree_and_rooftop_co2_values(self.request)
		eco_name = info_dict['biodome']
		latitude, longitude = GeoLocationUtil.tile_value_to_degree(
			self.request.x_grid_coord,
			self.request.y_grid_coord,
			20)
		carbon_storage_tree = info_dict['carbon_storage_tree']
		carbon_storage_rooftops = info_dict['carbon_storage_rooftops']
		oxygen_emission_tree = info_dict['oxygen_emission_tree']
		oxygen_emission_rooftop = info_dict['oxygen_emission_rooftop']
		carbon_emission_car = info_dict['carbon_emission_car']
		urban_cooling_tree = info_dict['urban_cooling_tree']
		urban_cooling_rooftop = info_dict['urban_cooling_rooftop']

		count_of_trees = 0
		count_of_cars = 0
		square_meters_of_rooftops = 0
		count_cars_swapped = 0

		for element in element_list:
			if isinstance(element, TreesLayer):
				count_of_trees = self.process_tree_layer(tree_layer=element)
			if isinstance(element, CarsLayer):
				count_of_cars = self.process_cars_layer(cars_layer=element)
			if isinstance(element, Scenario):
				count_trees_added, count_cars_swapped = self.process_scenario(scenario=element)
				count_of_trees += (count_trees_added + count_cars_swapped)
				count_of_cars += -count_cars_swapped

		total_carbon_storage = (count_of_trees * carbon_storage_tree) + (square_meters_of_rooftops * carbon_storage_rooftops)
		total_oxygen_emission = (count_of_trees * oxygen_emission_tree) + (square_meters_of_rooftops * oxygen_emission_rooftop)
		total_carbon_emission = count_of_cars * carbon_emission_car
		total_urban_cooling = (count_of_trees * urban_cooling_tree) + (square_meters_of_rooftops * urban_cooling_rooftop)

		result_string = "\n \n \n"
		result_string += "LOCATION \n \n"
		result_string += str(latitude) + ", " + str(longitude) + "\n"
		result_string += str(eco_name) + "\n \n"

		result_string += "FEATURES \n \n"
		result_string += "Trees: " + str(count_of_trees) + "  " + str(count_cars_swapped) + "\n"
		result_string += "Cars: " + str(count_of_cars) + "  " + str(-count_cars_swapped) + "\n"
		result_string += "Rooftops: " + str(square_meters_of_rooftops) + "m2" + "\n \n"

		result_string += "PERFORMANCE \n \n"
		result_string += "Biomass: CO2 storage:\n"
		result_string += str(total_carbon_storage) + " kg carbon " + "\n \n"

		result_string += "Air Quality: O2/CO2 Emission:\n"
		result_string += str(total_oxygen_emission) + " kg O2 " + "\n"
		result_string += str(total_carbon_emission) + " kg CO2 " + "\n \n"

		result_string += "Comfort: Urban Cooling:\n"
		result_string += str(total_urban_cooling) + " degrees kelvin" + "\n \n"

		return result_string
