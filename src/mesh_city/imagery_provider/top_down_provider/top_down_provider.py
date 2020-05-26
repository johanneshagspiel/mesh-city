"""
Module which takes care of the core functionality regarding importing top down imagery from
different API providers.
 """

from abc import ABC, abstractmethod


class TopDownProvider(ABC):
	"""
	An abstract class that provides the basic outline for more specific API providers for top-down
	imagery.
	"""

	def __init__(self, image_provider_entity):
		self.image_provider_entity = image_provider_entity
		self.padding = 0
		self.type = "top_down_provider"
		self.max_side_resolution_image = 0
		self.max_zoom = 16

		@abstractmethod
		def get_and_store_location():  # pylint: disable=unused-variable
			"""
			Method which makes an API call, and saves it in right format. Also removes the Google logo.
			:return:
			"""
