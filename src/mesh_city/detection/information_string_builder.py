"""
See class description
"""
import csv
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
		:param request_latitude: The latitude to look up the values for.
		:param request_longitude: The longitude to look up the values for.
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
						'carbon_emission_car': carbon_emission_car
					}
					info.append(dictionary)
		point = {'latitude': request_latitude, 'longitude': request_longitude}
		closest = GeoLocationUtil.closest(info, point)
		return closest

	def process_request(self, request: Request) -> str:
		"""
		Processes a request to turn it into an information string.
		:param request: The request to process
		:return: A multiline string representing statistics about the request
		"""
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
		"""
		Processes a scenario to turn it into an information string.
		:param scenario: The scenario to process
		:return: A multiline string representing statistics about the scenario
		"""
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
		Constructs a multiline information string based on a set of parameters.
		:param latitude: The approximate latitude of the region described by the parameters
		:param longitude: The approximate longitude of the region described by the parameters
		:param count_of_trees: The number of trees in the region
		:param count_of_cars: The number of cars in the region
		:param square_meters_of_rooftops: The area of rooftops in square meters prior to shrubification
		:param count_cars_swapped: The number of cars replaced by trees
		:param count_trees_added: The number of trees added in addition to these car swappings
		:param fraction_rooftops_greenified: The fraction of shrubified rooftops
		:return: An informative multiline string for use in the GUI
		"""
		info_dict = self.get_csv_biome_info(request_latitude=latitude, request_longitude=longitude)
		eco_name = info_dict['biodome']
		carbon_storage_tree = info_dict['carbon_storage_tree']
		carbon_storage_rooftops = info_dict['carbon_storage_rooftops']
		oxygen_emission_tree = info_dict['oxygen_emission_tree']
		oxygen_emission_rooftop = info_dict['oxygen_emission_rooftop']
		carbon_emission_car = info_dict['carbon_emission_car']

		count_trees_added = (count_trees_added + count_cars_swapped)
		area_of_green_rooftop = square_meters_of_rooftops * fraction_rooftops_greenified

		count_of_co2_stored_added = (count_trees_added *
			carbon_storage_tree) + (area_of_green_rooftop * carbon_storage_rooftops)
		count_of_o2_emission_added = (count_trees_added *
			oxygen_emission_tree) + (area_of_green_rooftop * oxygen_emission_rooftop)
		count_of_co2_emission_added = count_cars_swapped * carbon_emission_car

		total_count_of_trees = count_of_trees + count_trees_added
		total_count_of_cars = count_of_cars - count_cars_swapped

		detection_carbon_storage = (count_of_trees * carbon_storage_tree)
		detection_oxygen_emission = (count_of_trees * oxygen_emission_tree)
		detection_carbon_emission = count_of_cars * carbon_emission_car


		result_string = "\n \n \n"
		result_string += "LOCATION \n \n"
		result_string += str(latitude) + ", " + str(longitude) + "\n"
		result_string += str(eco_name) + "\n \n"

		result_string += "FEATURES \n \n"
		result_string += "Trees: " + str(count_of_trees) + "  + " + str(count_trees_added) + "\n"
		result_string += "Cars: " + str(count_of_cars) + "  - " + str(count_cars_swapped) + "\n"
		result_string += "Rooftops: " + str(int(square_meters_of_rooftops)) + "m2" + "\n"
		result_string += "Rooftops Greenified: " + str(
			int(square_meters_of_rooftops * fraction_rooftops_greenified)
		) + "m2" + "\n \n"

		result_string += "PERFORMANCE \n \n"
		result_string += "Biomass stored in trees. \nCO2 storage:\n"
		result_string += str(int(detection_carbon_storage)) + " kg carbon " + "\n"
		result_string += "Added:  + " + str(int(count_of_co2_stored_added)) + "\n \n"

		result_string += "Air Quality. \nO2 (by trees) and CO2 (by cars) Emissions:\n"
		result_string += str(int(detection_oxygen_emission)) + " kg O2 " + "\n"
		result_string += "Added:  + " + str(int(count_of_o2_emission_added)) + "\n"
		result_string += str(int(detection_carbon_emission)) + " kg CO2 " + "\n"
		result_string += "Decreased:  - " + str(int(count_of_co2_emission_added)) + "\n \n"

		return result_string
