from mesh_city.request.google_layer import GoogleLayer


class RequestManager:
	"""A class for storing previous requests and reusing their imagery"""

	def __init__(self, image_root,requests=[]):
		self.requests = requests
		self.images_root = image_root
		self.grid = {}
		for request in self.requests:
			self.update_grid(request)

	def add_request(self, request):
		self.requests.append(request)
		self.update_grid(request)

	def get_request_by_id(self, id):
		for request in self.requests:
			if request.request_id is id:
				return request
		raise ValueError("No request with this id exists")

	def get_image_root(self):
		return self.images_root

	def update_grid(self, request):
		if request.has_layer_of_type(GoogleLayer):
			google_layer = request.get_layer_of_type(GoogleLayer)
			for tile in google_layer.tiles:
				if not self.is_in_grid(tile.x_coord, tile.y_coord):
					self.add_path_to_grid(tile.x_coord, tile.y_coord, tile)

	def is_in_grid(self, latitude, longitude):
		return latitude in self.grid and longitude in self.grid[latitude]

	def add_path_to_grid(self, latitude, longitude, path):
		if not latitude in self.grid:
			self.grid[latitude] = {}
		self.grid[latitude][longitude] = path

	def get_path_from_grid(self, latitude, longitude):
		return self.grid[latitude][longitude]
