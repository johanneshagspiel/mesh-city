import json
from pathlib import Path

from mesh_city.user.entities.user_entity import UserEntity

class FileHandler:

	def __init__(self):
		self.root = Path(__file__).parents[1]
		self.folder_overview = {
			"resource_path" : Path.joinpath(self.root, 'resources'),
			"image_path" : Path.joinpath(self.root, 'images'),
			"users.json": Path.joinpath(self.root, 'resources', 'user', 'users.json'),
			"log_request_.json" : Path.joinpath(self.root, 'resources', 'logs', 'log_request_.json')
		}

	def file_exists(self):
		"""
		A method that check whether the file exists or not.
		"""
		try:
			self.load_user_info()
		except:
			return False
		else:
			return True
