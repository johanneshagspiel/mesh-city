import os
import json
from pathlib import Path
from datetime import datetime


class google_api_util:
	temp_path = Path(__file__).parents[2]
	api_file_path = Path.joinpath(temp_path, 'resources', 'api_key.json')

	def __init__(self):
		# If it's the first time that the user is entering their key and quota
		if (self.get_api_key()) == -1:
			self.api_key = input("Please enter your api-key\n")
			self.quota = input("Please enter your quota\n")
			self.name = input(
				"Please enter your name\n")  # A nickname for future entries
			self.usage = 0
			self.store_user_info(self.api_key, self.quota, self.usage, self.name)

		else:
			init_name = input("Please enter your name\n")
			if self.get_name() == init_name:
				self.api_key = self.get_api_key()
				self.quota = self.get_quota()
				self.name = self.get_name()
				print("Welcome " + self.name + " your quota is " + self.quota)

	def store_user_info(self, api_key, init_quota, usage_so_far, chosen_name):
		with open(self.api_file_path, 'w') as storage_json:
			user_info = {
				"name": chosen_name,
				"api_key": api_key,
				"quota": init_quota,
				"usage": usage_so_far,
				"year": datetime.now().year,
				"month": datetime.now().month,
				"day": datetime.now().day,
				"hour": datetime.now().hour,
				"minute": datetime.now().minute,
				"second": datetime.now().second
			}
			storage_json.write(json.dumps(user_info))
			storage_json.close()  # not sure if we need this line

	def get_user_info(self):
		with open(self.api_file_path, 'r') as storage_json:
			return json.loads(storage_json.read())

	def get_api_key(self):
		if (self.check_key_exist() & self.check_file_exist()) == False:
			print("There is no apy-key stored")
			return -1
		with open(self.api_file_path, 'r') as storage:
			user_info = json.loads(storage.read())
			return user_info["api_key"]

	def check_file_exist(self):
		if os.path.exists(self.api_file_path) == False:
			print("api-key.txt has been deleted - new file will be created")
			open(self.api_file_path, "x")
			return True
		return True

	def check_key_exist(self):
		if os.path.getsize(self.api_file_path) == 0:
			return False
		return True

	def check_usage_against_quota(self, old_usage):
		quota = int(self.quota)
		if (quota - old_usage) <= 100:
			print("Warning, you are getting close to your quota limit!")

	def check_monthly_limit(self):
		init_date = datetime(self.get_user_info()["year"],
		                     self.get_user_info()["month"],
		                     self.get_user_info()["day"])
		diff_months = datetime.now().month - init_date.month
		diff_days = datetime.now().day - init_date.day

		if diff_months == 0:
				# We good? or are there edge cases in the monthly billing?
			print("within the monthly limit")
		if diff_months == 1 & diff_days >= -3:
			print("You are getting close to the end of the month on your quota.")
		else:
			print("You should renew your quota.")

	def increase_usage(self):
		old_usage = self.usage
		self.check_usage_against_quota(old_usage)
		self.usage = old_usage + 1

	def get_quota(self):
		with open(self.api_file_path, 'r') as storage:
			user_info = json.loads(storage.read())
			return user_info["quota"]

	def get_name(self):
		with open(self.api_file_path, 'r') as storage:
			user_info = json.loads(storage.read())
			return user_info["name"]


def main():
	test = google_api_util()
	test.check_key_exist()


if __name__ == "__main__":
	main()
