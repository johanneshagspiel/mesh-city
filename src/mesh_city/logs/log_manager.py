"""
A module that contains the log manager who is responsible for performing all the actions associated with logs
"""

import json

from mesh_city.user.user_entity import UserEntity


class LogManager:
	"""
	A class that is responsible for logging every request made.
	"""

	def __init__(self, file_handler):
		self.file_handler = file_handler
		self.paths = file_handler.folder_overview

	def write_log(self, log_entry):
		"""
		A method to write one log entry entity to the associated correct location.

		:param log_entry: the log entry with its appropriate location to store it to
		:return: nothing
		"""

		with open(log_entry.path_to_store, "r") as json_log:
			data = json_log.read()
		logs = json.loads(data)
		result = log_entry.action(logs)

		with open(log_entry.path_to_store, "w") as json_log:
			json.dump(result, fp=json_log, indent=4)
			json_log.close()

	def create_log(self, log_entry):
		"""
		Method to store one new log
		:param log_entry: the log entry to store
		:return: nothing (the log is stored to file)
		"""
		with open(log_entry.path_to_store, "w") as json_log:
			json.dump(log_entry.for_json(), fp=json_log, indent=4)
			json_log.close()

	def read_log(self, path, type_document):
		"""
		Method to read what is at the path and then build it appropriately.

		:param path: the path where to load the log from
		:return: whatever the result of building that object is
		"""

		with open(path, "r") as json_log:
			data = json_log.read()
		logs = json.loads(data)

		temp_dic = {}

		if type_document == "users.json":
			for key, value in logs.items():
				temp_dic_entry = {key: value}
				temp_dic[key] = UserEntity(file_handler=self.file_handler, json=temp_dic_entry)
			return temp_dic

		return None

	def change_name(self, old_name: str, new_name: str):
		"""
		Changes the name of a user
		:param old_name: The old name of the user
		:param new_name: The new name of the user
		:return: None
		"""

		path = self.file_handler.folder_overview["users.json"]
		with open(path, "r") as json_log:
			data = json_log.read()
		logs = json.loads(data)

		temp_dic = {}
		for key, value in logs.items():
			temp_dic[key] = value
		temp_dic[new_name] = temp_dic.pop(old_name)

		with open(path, "w") as json_log:
			json.dump(temp_dic, fp=json_log, indent=4)
			json_log.close()
