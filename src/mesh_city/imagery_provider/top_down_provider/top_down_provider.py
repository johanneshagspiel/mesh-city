from abc import ABC, abstractmethod


class TopDownProvider(ABC):

	def __init__(self, user_info, quota_manager):
		self.user_info = user_info
		self.quota_manager = quota_manager
		self.padding = 0
		self.type = "top_down_provider"

		@abstractmethod
		def get_and_store_location(self, latitude, longitude, zoom, name):
			pass
