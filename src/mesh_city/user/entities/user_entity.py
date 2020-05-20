from mesh_city.util.logs.log_entry.log_entity import LogEntity
from mesh_city.user.entities.image_provider_entity import ImageProviderEntity

class UserEntity(LogEntity):

	def __init__(self, file_handler, json = None, name = None, image_providers = None):
		self.file_handler = file_handler
		self.path_to_store = file_handler.folder_overview["users.json"][0]
		if (name and image_providers != None):
			self.name = name
			self.image_providers = image_providers
			self.check_name()
		else:
			self.name = None
			self.image_providers = None
			self.load_json(json)

	def load_json(self, json):
		key, value = list(json.items())[0]
		self.name = key
		self.image_providers = {}
		self.load_image_providers(value)

	def load_image_providers(self, json):
		for item in json.items():
			self.image_providers[item[0]] = (ImageProviderEntity(self.file_handler, item[1]))

	def for_json(self):
		self.check_name()
		temp_image_providers = {}
		for key, value in self.image_providers.items():
			temp_image_providers[key] = value.for_json()

		return temp_image_providers

	def action(self, logs):
		to_store = self.for_json()
		logs[self.name] = to_store
		return logs

	def check_name(self):
		names = {}
		for key, value in self.image_providers.items():
			if key in names:
				old_name = key
				new_value = names[old_name] + 1
				new_name = str(old_name) + "_" + str(new_value)

				names[new_name] = 0
				names[old_name] = new_value

				# new_key = new_name
				# self.image_providers[new_key] = self.image_providers.pop(old_name)
				# names[old_name] = new_value
			else:
				names[key] = 0

			for key, value in names.items():
				print(key)
