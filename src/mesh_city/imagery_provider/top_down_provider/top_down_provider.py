from abc import ABC, abstractmethod


class TopDownProvider(ABC):
	temp_path = None
	images_folder_path = None

	def __init__(self, user_info, quota_manager):
		self.user_info = user_info
		self.quota_manager = quota_manager
		self.padding = 0
		self.type = "top_down_provider"
		self.max_side_resolution_image = 0

		@abstractmethod
		def get_and_store_location(
			latitude, longitude, zoom, filename, new_folder_path, width=None, height=None
		):
			pass
