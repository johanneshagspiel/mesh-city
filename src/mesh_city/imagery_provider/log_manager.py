import json
import os
import re
from datetime import datetime as dt
from pathlib import Path


class LogManager:
	"""
	A class that is reponsible for logging every request made. It can be
	"""
	temp_path = Path(__file__).parents[1]
	image_path = Path.joinpath(temp_path, 'resources', 'images')
	log_path = Path.joinpath(image_path, 'log_request.json')

	def __init__(self):
		pass

	def get_request_number(self):
		"""
		This method is needed because request manager needs to know the number of the next request
		to name the folder appropriately
		:return: the number of the next request
		"""
		with open(self.log_path, 'r') as json_log:
			data = json_log.read()
			json_log.close()
		logs = json.loads(data)
		max_log = 0

		# for item in logs.values():
		# 	for element in item:
		# 		if (int(element[0]["request_number"]) > max_log):
		# 		    max_log = int(element[0]["request_number"])

		max_directory = 0

		# for directory in os.listdir(self.image_path):
		# 	#temp_ending = directory.path.dirname(directory)
		# 	temp_ending = re.findall("(request_",directory)
		# 	if(len(temp_ending) > 0):
		# 		print(temp_ending)
		# temp_result = int(temp_ending[0])
		# if(temp_result > max_directory):
		# 	max_directory = temp_result

		return max_log > max_directory if max_log + 1 else max_directory

	def write_entry_log(
		self, request_number, user_info, map_entity, number_requests, bounding_box, coordinates
	):
		"""
		This method writes one request to the log
		:param request_number: the number of the request
		:param user_entity: the user that makes the request
		:param map_entity: the map provider that was used to make the request
		:param number_requests: how many map calls were made in this request
		:param bounding_box: the bounding box surrounding the area covered by the requests
		:param coordinates: the coordinates that were used to make each individual map call
		:return:
		"""
		if (map_entity.type == "top_down_provider"):
			temp = TopDownProviderLogEntry(
				request_number, user_info, map_entity, number_requests, bounding_box, coordinates
			)
			with open(self.log_path, 'r') as json_log:
				data = json_log.read()
			logs = json.loads(data)
			temp_to_add = temp.for_json()
			logs['top_down_provider'].append(temp_to_add)

			with open(self.log_path, 'w') as json_log:
				json.dump(logs, fp=json_log)


class TopDownProviderLogEntry:

	def __init__(
		self, request_number, user_info, map_entity, number_requests, bounding_box, coordinates
	):
		self.request_number = str(request_number)
		self.name_user = str(user_info.name)
		self.map_provider = str(map_entity.name)
		self.number_requests = str(number_requests)
		self.date = str(dt.now().day) + "/" + str(dt.now().month) + "/" + str(
			dt.now().year
		) + ", " + str(dt.now().hour) + ":" + str(dt.now().minute)
		self.bounding_box = str(bounding_box)
		self.coordinates = str(coordinates)

	def for_json(self):
		return [
			({
			"request_number": self.request_number
			}), ({
			"name_user": self.name_user
			}), ({
			"map_provider": self.map_provider
			}), ({
			"number_requests": self.number_requests
			}), ({
			"date": self.date
			}), ({
			"bounding_box": self.bounding_box
			}), ({
			"coordinates": self.coordinates
			})
		]
