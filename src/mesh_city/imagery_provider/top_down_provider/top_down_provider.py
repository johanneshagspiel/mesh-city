from abc import ABC, abstractmethod


class TopDownProvider(ABC):
	temp_path = None
	images_folder_path = None

	def __init__(self, user_entity):
		self.user_entity = user_entity
		self.padding = 0

		@abstractmethod
		def get_and_store_location(self, x, y, name):
			pass
