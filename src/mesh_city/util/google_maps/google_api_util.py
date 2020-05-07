import os
from pathlib import Path

class google_api_util:
	temp_path = Path(__file__).parents[2]
	api_file_path = Path.joinpath(temp_path, 'resources','api_key.txt')

	def __init__(self):
		self.quota = input("Please enter your quota\n")
		self.usage = 0

		if((self.get_api_key()) == -1):
			self.api_key = input("Please enter your api-key\n")
			self.store_api_Key(self.api_key)

		else:
			self.api_key = self.get_api_key()

	def store_api_Key(self, api_key):
		with open(self.api_file_path, 'w') as storage:
			storage.write(api_key)
			storage.close()

	def get_api_key(self):
		if((self.check_key_exist() & self.check_file_exist()) == False):
			print("There is no apy-key stored")
			return -1
		with open(self.api_file_path, 'r') as storage:
			return storage.readlines()

	def check_file_exist(self):
		if(os.path.exists(self.api_file_path) == False):
			print("api-key.txt has been deleted - new file will be created")
			open(self.api_file_path, "x")
			return True
		return True

	def check_key_exist(self):
		if(os.path.getsize(self.api_file_path) == 0):
			return False
		return True

	def check_usage_against_quota(self, oldUsage):
		if(self.quota - oldUsage) <= 100:
			print("Warning, you are getting close to your quota limit!")

	def increase_usage(self):
		old_usage = self.usage
		self.check_usage_against_quota(self, old_usage)
		self.usage = old_usage + 1
