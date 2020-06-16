import csv

from mesh_city.request.cars_layer import CarsLayer
from mesh_city.request.layer import Layer
from mesh_city.request.request import Request
from mesh_city.request.trees_layer import TreesLayer
from math import cos, asin, sqrt

from mesh_city.util.geo_location_util import GeoLocationUtil


class InfoGenerator:

	def __init__(self, bio_path ):
		self.bio_path = "mesh_city\resources\PlanetPainter_BiomeIndex.csv"




	def get_number_of_detections_in_layer(self, layer: Layer):
		if isinstance(layer, (TreesLayer, CarsLayer)):
			count = 0
			with open(str(layer.detections_path), newline='') as csv_file:
				csv_reader = csv.reader(csv_file, delimiter=',')
				for (index, row) in enumerate(csv_reader):
					if len(row) > 0 and index > 0:
						count += 1
			return count
		else:
			raise Exception("Should be a car or tree")



	def get_tree_co2_values(self, request: Request):
		info = []
		with open(str(self.bio_path), newline='') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=';')
			for (index, row) in enumerate(csv_reader):
				if len(row) > 0 and index > 0:
					latitude, longitude = float(row[8]), float(row[9])
					carbon_storage = float(row[11])

					dict = {'lat': latitude, 'long': longitude, 'carbon storage': carbon_storage}
					info.append(dict)

		latitude, longitude = GeoLocationUtil.tile_value_to_degree(268659, 173378, 20)
		# request.x_grid_coord, request.y_grid_coord, 20)
		point = {'lat': latitude, 'lon': longitude}
		self.closest(dict, point)

	def distance(self, lat1, lon1, lat2, lon2):
		p = 0.017453292519943295
		a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (
				1 - cos((lon2 - lon1) * p)) / 2
		return 12742 * asin(sqrt(a))

	def closest(self, data, v):
		return min(data, key=lambda p: self.distance(v['lat'], v['lon'], p['lat'], p['lon']))






	# def create_export_csv(self, request: Request, layer: Layer):
	# 	"""
	# 	Method which uses the information of the bounding box detections to create a csv file with
	# 	the centre points of the detections, which can be used for importation to QGIS
	# 	:param request: The request that contains the layer to be exported
	# 	:param layer: the layer that you want to export
	# 	:return: a path to the to be exported layer
	# 	"""
	# 	if isinstance(layer, TreesLayer):
	# 		label = "trees"
	# 	elif isinstance(layer, CarsLayer):
	# 		label = "cars"
	# 	else:
	# 		raise Exception("Should be a car or tree")
	#
	# 	detections_export_path = self.request_manager.get_image_root().joinpath(label)
	# 	detections_export_path.mkdir(parents=True, exist_ok=True)
	# 	layer.detections_export_path = detections_export_path.joinpath(
	# 		"detections_" + str(request.request_id) + "_export.csv"
	# 	)
	#
	# 	x_nw, y_nw = request.x_grid_coord, request.y_grid_coord
	#
	# 	csv_data = {'latitude': [], 'longitude': [], 'label': [], 'generated': []}
	# 	with open(str(layer.detections_path), newline='') as csv_file:
	# 		csv_reader = csv.reader(csv_file, delimiter=',')
	# 		for (index, row) in enumerate(csv_reader):
	# 			if len(row) > 0 and index > 0:
	# 				xmin, ymin = float(row[1]), float(row[2])
	# 				xmax, ymax = float(row[3]), float(row[4])
	#
	# 				latitude, longitude = GeoLocationUtil.pixel_to_geo_coor(
	# 					x_nw, y_nw, xmin, ymin, xmax, ymax
	# 				)
	# 				csv_data['latitude'].append(latitude)
	# 				csv_data['longitude'].append(longitude)
	# 				csv_data['label'].append(label)
	# 				csv_data['generated'].append(0)
	#
	# 	pd.DataFrame(csv_data).to_csv(str(layer.detections_export_path), index=False)
	#
	# 	return layer.detections_export_path
