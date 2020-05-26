from mesh_city.logs.log_entities.log_entry import LogEntry

class CoordinateOverview(LogEntry):

	def __init__(self, path_to_store, json=None):
		super().__init__(path_to_store=path_to_store)
		if json is None:
			self.grid ={}
		else:
			self.grid = {}
			self.load_json(json)

	def action(self, logs):
		return self.for_json()

	def load_json(self, json):
		self.grid = json

	def for_json(self):
		return self.grid


