import json
from pathlib import Path
from mesh_city.user.user_info import UserInfo

class UserInfoHandler:

	def __init__(self):
		self.api_file_path = Path.joinpath(
			Path(__file__).parents[1], "resources", "user", "api_key.json"
		)

	def store_user_info(self, user_info):
		with open(self.api_file_path, "w") as storage_json:
			storage_json.write(json.dumps(user_info.__dict__))

	def load_user_info(self):
		with open(self.api_file_path, "r") as storage_json:
			info = UserInfo(**json.loads(storage_json.read()))
			return info

	def file_exists(self):
		try:
			self.load_user_info()
		except:
			return False
		else:
			return True
