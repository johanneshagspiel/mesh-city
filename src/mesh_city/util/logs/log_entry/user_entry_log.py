from mesh_city.util.logs.log_entry.log_entry import LogEntry

class UserEntryLog(LogEntry):

	def __init__(self, path_to_store, name, image_providers):
		self.path_to_store = path_to_store
		self.name = name
		self.image_providers = image_providers

	def for_json(self):
		self.check_name()
		return {
			self.name : {
			self.image_providers.for_json(),
			}
		}

	def action(self, logs):
			return self.for_json()

	def check_name(self):
		names = {}
		for entry in self.image_providers:
			if entry.name in names:
				old_name = entry.name
				new_value = names[old_name] + 1
				new_name = str(old_name) + "_" + str(new_value)
				entry.name = new_name
				names[old_name] = new_value
			else:
				names[entry.name] = 0
