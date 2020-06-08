class Request:
	"""Stores all relevant data of a request"""

	def __init__(self, request_id, width, height, x_coord, y_coord,zoom):
		self.request_id = request_id
		self.x_coord = x_coord
		self.y_coord = y_coord
		self.width = width
		self.height = height
		self.zoom = zoom
		self.layers = []

	def add_layer(self, layer):
		self.layers.append(layer)

	def has_layer_of_type(self, layer_type):
		for layer in self.layers:
			if isinstance(layer, layer_type):
				return True
		return False

	def get_layer_of_type(self, layer_type):
		for layer in self.layers:
			if isinstance(layer, layer_type):
				return layer
		raise ValueError("No layer of type " + str(layer_type) + " exists")
