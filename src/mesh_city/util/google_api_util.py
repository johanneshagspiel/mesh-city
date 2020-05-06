import os

class google_api_util:
	api_key = "test-value"
	quota = 0

	def __init__(self):
		if((self.getApi_Key()) == -1):
			self.api_key = input("Please enter your api-key")
			self.storeApi_Key(self.api_key)

		else:
			self.api_key = self.getApi_Key()

	def storeApi_Key(self, api_key):
		with open('src/mesh_city/resources/api_key.txt', 'w') as storage:
			storage.write(api_key)
			storage.close()

	def getApi_Key(self):
		if((self.checkKeyExist() & self.checkFileExist()) == False):
			print("There is no apy-key stored")
			return -1
		with open('src/mesh_city/resources/api_key.txt', 'r') as storage:
			return storage.readlines()

	def checkFileExist(self):
		if(os.path.exists('src/mesh_city/resources/api_key.txt', 'w') == False):
			print("api-key.txt has been deleted - new file will be created")
			open('src/mesh_city/resources/api_key.txt', "x")
		True

	def checkKeyExist(self):
		if(os.path.getsize('src/mesh_city/resources/api_key.txt') == 0):
			False
		True

def main():
	test = google_api_util()
	test.checkKeyExist()

if __name__ == "__main__":
       main()
