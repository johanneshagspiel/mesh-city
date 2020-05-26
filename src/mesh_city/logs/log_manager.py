"""
A module that contains the log manager who is responsible for performing all the actions associated with logs
"""

import json
import os
from pathlib import Path

from mesh_city.user.entities.user_entity import UserEntity


class LogManager:
	"""
	A class that is responsible for logging every request made.
	"""

	def __init__(self, file_handler, resource_path=Path(__file__).parents[1].joinpath("resources")):
		self.resource_path = resource_path
		self.image_path = resource_path.joinpath("images")
		self.log_path = resource_path.joinpath("logs", "log_request_.json")
		self.file_handler = file_handler

	def get_request_number(self):
		"""
		This method is needed because request manager needs to know the number of the next request
		to name the folder appropriately
		:return: the number of the next request
		"""

		max_log = 0

		if self.log_path.is_file():  # pylint: disable=no-member
			with open(self.log_path, "r") as json_log:
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

		self.image_path.mkdir(exist_ok=True)
		if len(os.listdir(self.image_path)) == 0:
			max_directory = 0
		else:
			for directory in os.listdir(self.image_path):
				if directory.split("_")[1] != "":
					temp_result = int(directory.split("_")[1])
					if temp_result > max_directory:
						max_directory = temp_result

		return max_log + 1 if max_log > max_directory else max_directory + 1

	def write_log(self, log_entry):
		"""
		A method to write one log entry entity to the associated correct location
		:param log_entry: the log entry with its appropriate location to store it to
		:return: nothing
		"""

		with open(log_entry.path_to_store, "r") as json_log:
			data = json_log.read()
		logs = json.loads(data)
		result = log_entry.action(logs)

		with open(log_entry.path_to_store, "w") as json_log:
			json.dump(result, fp=json_log)
			json_log.close()

	def read_log(self, path):
		"""
		Method to read what is at the path and then build it appropriately
		:param path: the path where to load the log from
		:return: whatever the result of building that object is
		"""
		with open(path[0], "r") as json_log:
			data = json_log.read()
		logs = json.loads(data)

		temp_dic = {}

		if path[1] == "users.json":
			print(logs.items())
			for key, value in logs.items():
				print(value)
				temp_dic[key] = UserEntity(
					file_handler=self.file_handler, name=key, json={key: value}
				)
			return temp_dic

		return logs
