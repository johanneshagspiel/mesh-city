from mesh_city.request.cars_layer import CarsLayer
from mesh_city.request.request import Request
from mesh_city.request.trees_layer import TreesLayer


class InfoGenerator:


	def get_number_of_trees_in_request(self, request: Request, layer: TreesLayer):
		if isinstance(layer, (TreesLayer, CarsLayer)):
			origin_path = layer.detections_path

