"""
See class description
"""
import csv
from pathlib import Path

from mesh_city.request.entities.request import Request
from mesh_city.request.layers.cars_layer import CarsLayer
from mesh_city.request.layers.trees_layer import TreesLayer
from mesh_city.util.geo_location_util import GeoLocationUtil


class InformationPipeline:
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

		latitude, longitude = GeoLocationUtil.tile_value_to_degree(request.x_grid_coord, request.y_grid_coord, 20)
		point = {'latitude': latitude, 'longitude': longitude}

		closest = GeoLocationUtil.closest(info, point)

		print(latitude, longitude)
		print('closest', closest)

		return closest

	def process_tree_layer(self, treeLayer: TreesLayer):

		count = 0
		with open(str(treeLayer.detections_path), newline='') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for (index, row) in enumerate(csv_reader):
				if len(row) > 0 and index > 0:
					count += 1
		self.result_string += "Trees Detected: " + str(count) + "\n"

	def process_cars_layer(self, carsLayer: CarsLayer):

		count = 0
		with open(str(carsLayer.detections_path), newline='') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for (index, row) in enumerate(csv_reader):
				if len(row) > 0 and index > 0:
					count += 1
		self.result_string += "Cars Detected: " + str(count) + "\n"

	def process(self, request: Request, element_list) -> str:

		self.result_string = ""

		for element in element_list:
			if isinstance(element, TreesLayer):
				self.process_tree_layer(treeLayer=element)
			if isinstance(element, CarsLayer):
				self.process_cars_layer(carsLayer=element)

		return self.result_string
