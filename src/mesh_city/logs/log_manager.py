"""
A module that contains the log manager who is responsible for performing all the actions associated with logs
"""

import json
import os

from mesh_city.user.entities.user_entity import UserEntity


class LogManager:
	"""
	A class that is responsible for logging every request made.
	"""

	def __init__(self, file_handler):
		self.file_handler = file_handler
		self.paths = file_handler.folder_overview

	def get_request_number(self):
		"""
		This method is needed because request manager needs to know the number of the next request
		to name the folder appropriately.

		:return: the number of the next request
		"""

		max_log = 0

		if self.paths["log_request_.json"].is_file():
			with open(self.paths["log_request_.json"], "r") as json_log:
				data = json_log.read()
				json_log.close()
			logs = json.loads(data)

			for item in logs.values():
				for element in item:
					element = [int(k) for k, v in element.items()][0]
					if element > max_log:
						max_log = element

		else:
			max_log = 0

		max_directory = 0

		temp_path = self.paths["image_path"]

		if len(os.listdir(self.paths["image_path"])) == 0:
			max_directory = 0
		else:
			for temp in temp_path.glob("*"):
				if temp.is_file():
					continue
				directory = temp.name
				if directory.split("_")[1] == '':
					continue
				temp_result = int(directory.split("_")[1])
				if temp_result > max_directory:
					max_directory = temp_result

		return max_log + 1 if max_log > max_directory else max_directory + 1

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

	def change_name(self, old_name, new_name):

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
