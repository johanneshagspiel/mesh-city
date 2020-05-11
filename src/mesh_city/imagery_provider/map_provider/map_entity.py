from abc import ABC, abstractmethod
from pathlib import Path

class MapEntity(ABC):
	temp_path = None
	images_folder_path = None

	def  __init__(self, user_entity):
		self.user_entity = user_entity
		self.temp_path = Path(__file__).parents[2]
		self.images_folder_path = Path.joinpath(self.temp_path, 'resources', 'images')
		self.padding = 0

		@abstractmethod
		def get_and_store_location(self, x, y, name):
			pass
