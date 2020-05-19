from abc import ABC, abstractmethod


class TopDownProvider(ABC):

	def __init__(self, image_provider_entity):
		self.image_provider_entity = image_provider_entity
		self.padding = 0
		self.type = "top_down_provider"
		self.max_side_resolution_image = 0

		@abstractmethod
		def get_and_store_location(
			latitude, longitude, zoom, filename, new_folder_path, width=None, height=None
		):
			pass
