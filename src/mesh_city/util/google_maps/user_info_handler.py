import json
import os
from datetime import datetime
from pathlib import Path

from mesh_city.util.google_maps.user_info import UserInfo


class UserInfoHandler:
	temp_path = Path(__file__).parents[2]
	api_file_path = Path.joinpath(temp_path, 'resources', 'api_key.json')

	def store_user_info(self, api_key, init_quota, usage_so_far, chosen_name):
		with open(self.api_file_path, 'w') as storage_json:
			storage_json.write(json.dumps(self.user_info.__dict__))

	def load_user_info(self):
		with open(self.api_file_path, 'r') as storage_json:
			return UserInfo(**json.loads(storage_json.read()))

	def user_info_file_exists(self):
		try:
			self.load_user_info()
			return True
		except:
			return False

	# def get_api_key(self):
	# 	if not (self.check_file_exist() and self.check_key_exist()):
	# 		print("There is no api-key stored")
	# 		return -1
	# 	with open(self.api_file_path, 'r') as storage:
	# 		self.increase_usage()  # Temporary place for increasing usage.
	# 		user_info = json.loads(storage.read())
	# 		return user_info["api_key"]

	# def check_file_exist(self):
	# 	if not os.path.exists(self.api_file_path):
	# 		print("api-key.txt has been deleted - new file will be created")
	# 		open(self.api_file_path, "x")
	# 		return True
	# 	return True
	#
	# def check_key_exist(self):
	# 	if os.path.getsize(self.api_file_path) == 0:
	# 		return False
	# 	return True
