from abc import ABC, abstractmethod

class TopDownProvider(ABC):
	temp_path = None
	images_folder_path = None

	def __init__(self, user_manager):
		self.user_manager = user_manager
		self.padding = 0
		self.type = "top_down_provider"

		@abstractmethod
		def get_and_store_location(self, longitude, latitutde, name):
			pass
