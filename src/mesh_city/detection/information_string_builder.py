"""
See class description
"""
import csv
from math import floor, log10
from pathlib import Path

import geopandas as gpd
import pandas as pd

from mesh_city.request.entities.request import Request
from mesh_city.request.layers.buildings_layer import BuildingsLayer
from mesh_city.request.layers.cars_layer import CarsLayer
from mesh_city.request.layers.trees_layer import TreesLayer
from mesh_city.scenario.scenario import Scenario
from mesh_city.util.geo_location_util import GeoLocationUtil


class InformationStringBuilder:
	"""
	Class which contains methods to count, analyse and create some statistics of the detections
	saved in layers of a request.
	"""

	def __init__(self, bio_path: Path):
		self.bio_path = bio_path

	def get_csv_biome_info(self, request_latitude, request_longitude) -> dict:
		"""
		Analyses the biome information csv and the coordinates of the current request so that it
		returns the point in the PlanetPainter_BiomIndex.csv file, closest to the coordinates of the
		request
		:param request_longitude: the relevant request's longitude coordinate
		:param request_latitude: the relevant request's latitude coordinate
		:return: a dictionary with the following fields with info:
		e'biodome': eco_name,
		'latitude': latitude,
		'longitude': longitude,
		'carbon_storage_tre': carbon_storage_tree,
		'carbon_storage_rooftops': carbon_storage_rooftops,
		'oxygen_emission_tree': oxygen_emission_tree,
		'oxygen_emission_rooftop': oxygen_emission_rooftop,
		'carbon_emission_car': carbon_emission_car,
		'urban_cooling_tree': urban_cooling_tree,
		'urban_cooling_rooftop': urban_cooling_rooftop
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
		point = {'latitude': request_latitude, 'longitude': request_longitude}
		closest = GeoLocationUtil.closest(info, point)
		return closest

	def process_request(self, request: Request) -> str:
		count_of_trees = 0
		count_of_cars = 0
		square_meters_of_rooftops = 0

		latitude, longitude = GeoLocationUtil.tile_value_to_degree(
			request.x_grid_coord,
			request.y_grid_coord,
			20)
		if request.has_layer_of_type(TreesLayer):
			count_of_trees = len(pd.read_csv(request.get_layer_of_type(TreesLayer).detections_path))
		if request.has_layer_of_type(CarsLayer):
			count_of_cars = len(pd.read_csv(request.get_layer_of_type(CarsLayer).detections_path))
		if request.has_layer_of_type(BuildingsLayer):
			building_dataframe = gpd.read_file(
				request.get_layer_of_type(BuildingsLayer).detections_path
			)
			for polygon in building_dataframe["geometry"]:
				square_meters_of_rooftops += polygon.area
			square_meters_of_rooftops *= GeoLocationUtil.calc_meters_per_px(
				latitude=latitude, zoom=20, image_resolution=1024
			)**2
		latitude, longitude = GeoLocationUtil.tile_value_to_degree(request.x_grid_coord,
			request.y_grid_coord,
			20)
		return self.process(
			latitude=latitude,
			longitude=longitude,
			count_of_trees=count_of_trees,
			count_of_cars=count_of_cars,
			square_meters_of_rooftops=square_meters_of_rooftops
		)

	def process_scenario(self, scenario: Scenario) -> str:
		count_of_trees = 0
		count_of_cars = 0
		count_trees_added = 0
		square_meters_of_rooftops = 0
		count_cars_swapped = 0
		percentage_of_rooftops_greenified = 0
		latitude, longitude = GeoLocationUtil.tile_value_to_degree(
			scenario.request.x_grid_coord,
			scenario.request.y_grid_coord,
			20)
		if scenario.trees is not None:
			count_cars_swapped = len(scenario.trees.loc[scenario.trees['label'] == "SwappedCar"])
			count_trees_added = len(scenario.trees.loc[scenario.trees['label'] == "AddedTree"])
			count_of_trees = len(scenario.trees.loc[scenario.trees['label'] == "Tree"])
		if scenario.cars is not None:
			count_of_cars = len(scenario.cars)
		if scenario.buildings is not None:
			green_area = 0
			pixel_area_to_m2 = GeoLocationUtil.calc_meters_per_px(
				latitude=latitude, zoom=20, image_resolution=1024
			)**2
			for polygon in scenario.buildings.loc[scenario.buildings['label'] == "Shrubbery"
													].geometry:
				green_area += polygon.area
			for polygon in scenario.buildings.geometry:
				square_meters_of_rooftops += polygon.area
			percentage_of_rooftops_greenified = green_area / square_meters_of_rooftops
			square_meters_of_rooftops *= pixel_area_to_m2
			green_area *= pixel_area_to_m2

		latitude, longitude = GeoLocationUtil.tile_value_to_degree(scenario.request.x_grid_coord,
			scenario.request.y_grid_coord,
			20)
		return self.process(
			latitude=latitude,
			longitude=longitude,
			count_of_trees=count_of_trees,
			count_of_cars=count_of_cars + count_cars_swapped,
			square_meters_of_rooftops=square_meters_of_rooftops,
			count_cars_swapped=count_cars_swapped,
			count_trees_added=count_trees_added,
			fraction_rooftops_greenified=percentage_of_rooftops_greenified
		)

	def process(
		self,
		latitude,
		longitude,
		count_of_trees: int,
		count_of_cars: int,
		square_meters_of_rooftops: int,
		count_cars_swapped: int = 0,
		count_trees_added: int = 0,
		fraction_rooftops_greenified: float = 0
	) -> str:
		"""
		Processes a list of elements that can be either Layers or Scenarios
		:param element_list: The list of Layers and/or Scenarios
		:return: An information string with all the statistics of the request/scenario
		"""
		info_dict = self.get_csv_biome_info(request_latitude=latitude, request_longitude=longitude)
		eco_name = info_dict['biodome']
		carbon_storage_tree = info_dict['carbon_storage_tree']
		carbon_storage_rooftops = info_dict['carbon_storage_rooftops']
		oxygen_emission_tree = info_dict['oxygen_emission_tree']
		oxygen_emission_rooftop = info_dict['oxygen_emission_rooftop']
		carbon_emission_car = info_dict['carbon_emission_car']
		urban_cooling_tree = info_dict['urban_cooling_tree']
		urban_cooling_rooftop = info_dict['urban_cooling_rooftop']

		count_of_trees += (count_trees_added + count_cars_swapped)
		count_of_cars += -count_cars_swapped
		total_carbon_storage = (count_of_trees *
			carbon_storage_tree) + (square_meters_of_rooftops * carbon_storage_rooftops)
		total_oxygen_emission = (count_of_trees *
			oxygen_emission_tree) + (square_meters_of_rooftops * oxygen_emission_rooftop)
		total_carbon_emission = count_of_cars * carbon_emission_car
		total_urban_cooling = (count_of_trees * urban_cooling_tree) + (
			square_meters_of_rooftops * fraction_rooftops_greenified * urban_cooling_rooftop
		)
		total_urban_cooling = InformationStringBuilder.round_sig(total_urban_cooling, 5)

		result_string = "\n \n \n"
		result_string += "LOCATION \n \n"
		result_string += str(latitude) + ", " + str(longitude) + "\n"
		result_string += str(eco_name) + "\n \n"

		result_string += "FEATURES \n \n"
		result_string += "Trees: " + str(count_of_trees) + "  +" + str(count_cars_swapped) + "\n"
		result_string += "Cars: " + str(count_of_cars) + "  -" + str(count_cars_swapped) + "\n"
		result_string += "Rooftops: " + str(int(square_meters_of_rooftops)) + "m2" + "\n"
		result_string += "Rooftops Greenified: " + str(
			int(square_meters_of_rooftops * fraction_rooftops_greenified)
		) + "m2" + "\n \n"

		result_string += "PERFORMANCE \n \n"
		result_string += "Biomass. \nCO2 storage:\n"
		result_string += str(int(total_carbon_storage)) + " kg carbon " + "\n \n"

		result_string += "Air Quality. \nO2/CO2 Emission:\n"
		result_string += str(int(total_oxygen_emission)) + " kg O2 " + "\n"
		result_string += str(int(total_carbon_emission)) + " kg CO2 " + "\n \n"

		result_string += "Comfort. \nUrban Cooling:\n"
		result_string += str(total_urban_cooling) + " degrees kelvin" + "\n \n"

		return result_string

	@staticmethod
	def round_sig(number, sig=2):
		"""
		A simple helper function to round numbers to a certain number of decimal places.
		:param number: number to round.
		:param sig: number of significant digits.
		:return: the number with the right number of significant digits
		"""
		return round(number, sig - int(floor(log10(abs(number)))) - 1)
