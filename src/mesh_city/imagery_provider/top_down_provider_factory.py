"""
Module which provides a simple factory to create different types of TopDownProvider's.
"""

from mesh_city.imagery_provider.top_down_provider.google_maps_provider import GoogleMapsProvider
from mesh_city.imagery_provider.top_down_provider.mapbox_provider import MapboxProvider


class TopDownProviderFactory:
	"""
	A class that created different kinds of TopDownProvider's
	"""

	@staticmethod
	def get_top_down_provider(image_provider_entity):
		"""
		Constructs a TopDownProvider instance using an ImageProviderEntity instance.

		:param image_provider_entity: The ImageProviderEntity to instantiate the TopDownProvider with.
		:return: A TopDownProvider instance.
		"""

		if image_provider_entity.type == "Google Maps":
			return GoogleMapsProvider(image_provider_entity=image_provider_entity)
		if image_provider_entity.type == "Mapbox":
			return MapboxProvider(image_provider_entity=image_provider_entity)
		raise ValueError("This image provider type_of_detection is not defined")
