import os
from pathlib import Path

class google_api_util:
	api_key = "test-value"
	quota = 0
	resource_folder = os.path.dirname(__file__)
	api_file_path = os.path.relpath('..\\resources\\api_key.txt', resource_folder)

	def __init__(self):
		self.quota = input("Please enter your quota\n")

		if((self.getApi_Key()) == -1):
			self.api_key = input("Please enter your api-key\n")
			self.storeApi_Key(self.api_key)

		else:
			self.api_key = self.getApi_Key()

	def storeApi_Key(self, api_key):
		with open(self.api_file_path, 'w') as storage:
			storage.write(api_key)
			storage.close()

	def getApi_Key(self):
		if((self.checkKeyExist() & self.checkFileExist()) == False):
			print("There is no apy-key stored")
			return -1
		with open(self.api_file_path, 'r') as storage:
			return storage.readlines()

	def checkFileExist(self):
		if(os.path.exists(self.api_file_path) == False):
			print("api-key.txt has been deleted - new file will be created")
			open(self.api_file_path, "x")
			return True
		return True

	def checkKeyExist(self):
		if(os.path.getsize(self.api_file_path) == 0):
			return False
		return True
