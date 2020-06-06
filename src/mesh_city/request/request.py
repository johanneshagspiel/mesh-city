class Request:
	"""Stores all relevant data of a request"""

	def __init__(self, request_id):
		self.request_id = request_id
		self.layers = []

	def add_layer(self, layer):
		self.layers.append(layer)
