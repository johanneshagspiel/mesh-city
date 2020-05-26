"""
A module that contains the log manager who is responsible for performing all the actions associated with logs
"""

import json
import os

from mesh_city.user.entities.user_entity import UserEntity
from mesh_city.logs.log_entities.coordinate_overview import CoordinateOverview


class LogManager:
	"""
	A class that is reponsible for logging every request made. It can be
	"""

	def __init__(self, file_handler):
		"""
		Initializes a log_manager method
		"""
		self.paths = file_handler.folder_overview
		self.file_handler = file_handler

	def get_request_number(self):
		"""
		This method is needed because request manager needs to know the number of the next request
		to name the folder appropriately
		:return: the number of the next request
		"""

		max_log = 0

		if (self.paths["log_request_.json"][0].is_file()):
			with open(self.paths["log_request_.json"][0], 'r') as json_log:
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

		temp_path = self.paths["image_path"][0]

		if (len(os.listdir(self.paths["image_path"][0])) == 0):
			max_directory = 0
		else:
			for temp in temp_path.glob('*'):
				if temp.is_file() is False:
					directory = temp.name
					if (directory.split("_")[1] != ''):
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
			json.dump(result, fp=json_log, indent=4)
			json_log.close()

	def create_log(self, log_entry):
		with open(log_entry.path_to_store, "w") as json_log:
			json.dump(log_entry.for_json(), fp=json_log, indent=4)
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
			for key, value in logs.items():
				temp_dic_entry = {key: value}
				temp_dic[key] = UserEntity(file_handler=self.file_handler, json=temp_dic_entry)
			return temp_dic

		if path[1] == "coordinate_overview.json":
			temp_coordinate_overview = CoordinateOverview(path_to_store=self.file_handler.folder_overview["coordinate_overview.json"][0], json=logs)
			self.file_handler.coordinate_overview = temp_coordinate_overview

		return logs
