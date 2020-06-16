"""
See class description
"""
import csv
from pathlib import Path

from mesh_city.request.cars_layer import CarsLayer
from mesh_city.request.layer import Layer
from mesh_city.request.request import Request
from mesh_city.request.trees_layer import TreesLayer
from mesh_city.util.geo_location_util import GeoLocationUtil


class InfoGenerator:
	"""
	Class which contains methods to count, analyse and create some statistics of the detections
	saved in layers of a request.
	"""

	def __init__(self, bio_path: Path, request: Request):
		self.bio_path = bio_path
		self.request = request

	def get_number_of_cars_and_trees(self):
		"""
		Analyses a request to
		:return: the number of trees and cars detected in that request
		"""
		layers = self.request.layers
		trees = None
		cars = None

		for layer in layers:
			if isinstance(layer, TreesLayer):
				trees = self.get_number_of_detections_in_layer(layer)
			if isinstance(layer, CarsLayer):
				cars = self.get_number_of_detections_in_layer(layer)

		return {'trees': trees, 'cars': cars}

	def get_number_of_detections_in_layer(self, layer: Layer):
		"""
		Analyses a layer to count the number of detections of a certain class in the layer.
		:param layer: the layer to be analysed
		:return: the number of detections in the images of the respective class of layer
		"""
		if isinstance(layer, (TreesLayer, CarsLayer)):
			count = 0
			with open(str(layer.detections_path), newline='') as csv_file:
				csv_reader = csv.reader(csv_file, delimiter=',')
				for (index, row) in enumerate(csv_reader):
					if len(row) > 0 and index > 0:
						count += 1
			return count
		raise Exception("Should be a car or tree")

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
