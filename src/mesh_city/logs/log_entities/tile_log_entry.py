from mesh_city.logs.log_entities.log_entry import LogEntry

class TileLogEntry(LogEntry):

	def __init__(self, path_to_store, json=None, name=None):
		super().__init__(path_to_store=path_to_store)

		if name is not None:
			self.name = name
			self.general_information={}
			self.layer_information = {}
		else:
			self.name = None
			self.general_information = {}
			self.layer_information = {}
			self.load_json(json)

	def load_json(self, json):
		return None

	def action(self, logs):
		return self.for_json()

	def for_json(self):
		return {self.name : {
			"general_information" : self.general_information,
			"layer_information" : self.layer_information
			}
		}
