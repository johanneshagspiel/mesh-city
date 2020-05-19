"""
See :class:`.UserInfoHandler`
"""

import json
from pathlib import Path

from mesh_city.user.user_info import UserInfo


class UserInfoHandler:
	"""
	A class that can store and load user information.
	"""

	def __init__(self, resource_path: str = None):
		if resource_path is None:
			self.api_file_path = Path.joinpath(
				Path(__file__).parents[1], "resources", "user", "api_key.json"
			)
		else:
			self.api_file_path = resource_path

	def store_user_info(self, user_info):
		"""
		A method that stores user information in a json format.
		:param user_info: The user information

		"""
		with open(self.api_file_path, "w") as storage_json:
			storage_json.write(json.dumps(user_info.__dict__))

	def load_user_info(self):
		"""
		A method that load user information from a json format.
		"""
		with open(self.api_file_path, "r") as storage_json:
			info = UserInfo(**json.loads(storage_json.read()))
			return info

	def file_exists(self):
		"""
		A method that check whether the file exists or not.
		"""
		try:
			self.load_user_info()
		except (OSError, ValueError, TypeError):
			return False
		else:
			return True
