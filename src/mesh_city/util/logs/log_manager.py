"""
A module that contains the log manager who is responsible for performing all the actions associated with logs
"""
import json
import os
from pathlib import Path

class LogManager:
	"""
	A class that is reponsible for logging every request made. It can be
	"""

	def __init__(self, file_handler):
		"""
		Initializes a log_manager method
		"""
		self.paths = file_handler.folder_overview

	def get_request_number(self):
		"""
		This method is needed because request manager needs to know the number of the next request
		to name the folder appropriately
		:return: the number of the next request
		"""
		max_log = 0

		if (self.paths["log_request_.json"].is_file()):
			with open(self.paths["log_request_.json"], 'r') as json_log:
				data = json_log.read()
				json_log.close()
			logs = json.loads(data)

			for item in logs.values():
				for element in item:
					element = [int(k) for k, v in element.items()][0]
					if (element > max_log):
						max_log = element

		else:
			max_log = 0

		max_directory = 0

		if (len(os.listdir(self.paths["image_path"])) == 0):
			max_directory = 0
		else:
			for directory in os.listdir(self.paths["image_path"]):
				if (directory.split("_")[1] != ''):
					temp_result = int(directory.split("_")[1])
					if (temp_result > max_directory):
						max_directory = temp_result

		return max_log + 1 if max_log > max_directory else max_directory + 1

	def write_log(self, logEntry):
		"""
		A method to write one log entry entity to the associated correct location
		:param logEntry: the log entry with its appropriate location to store it to
		:return: nothing
		"""

		with open(logEntry.path_to_store, "r") as json_log:
			data = json_log.read()
		logs = json.loads(data)
		result = logEntry.action(logs)

		with open(logEntry.path_to_store, "w") as json_log:
			json.dump(result, fp=json_log)
			json_log.close()

	def read_log(path):
		with open(path, "r") as json_log:
			data = json_log.read()
		return json.loads(data)
