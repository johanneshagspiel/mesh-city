"""
See :class:`.Request`
"""

from typing import Any

from mesh_city.request.layer import Layer


class Request:
	"""Stores all relevant data of a request"""

	def __init__(self, request_id, width, height, x_coord, y_coord, zoom, layers=None) -> None:
		self.request_id = request_id
		self.x_coord = x_coord
		self.y_coord = y_coord
		self.width = width
		self.height = height
		self.zoom = zoom
		self.layers = [] if layers is None else layers

	def add_layer(self, layer: Layer) -> None:
		"""
		Adds a layer to this request.

		:param layer: the layer that is to be added
		:return: None
		"""
		self.layers.append(layer)

	def has_layer_of_type(self, layer_type: type) -> bool:
		"""
		Returns whether this request has a layer of the given type or not.

		:param layer_type: The type of layer to check for
		:return: None
		"""
		for layer in self.layers:
			if isinstance(layer, layer_type):
				return True
		return False

	def get_layer_of_type(self, layer_type: type) -> Any:
		"""
		Tries to get a layer of the specified type.

		:param layer_type: The type of layer to get an instance of
		:return: An instance of this layer type if the class has one, else errors. Typed as Any
		         because of type system limitations.
		"""
		for layer in self.layers:
			if isinstance(layer, layer_type):
				return layer
		raise ValueError("No layer of type " + str(layer_type) + " exists")
