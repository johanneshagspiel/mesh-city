"""
Module which provides a simple factory to create different types of TopDownProvider's.
"""

from mesh_city.imagery_provider.top_down_provider.ahn_provider import AhnProvider
from mesh_city.imagery_provider.top_down_provider.google_maps_provider import GoogleMapsProvider
from mesh_city.imagery_provider.top_down_provider.mapbox_provider import MapboxProvider


class TopDownProviderFactory:
	"""
	A class that created different kinds of TopDownProvider's
	"""

	def get_top_down_provider(self, image_provider_entity):
		"""
		Constructs a TopDownProvider instance using an ImageProviderEntity instance
		:param image_provider_entity: The ImageProviderEntity to instantiate the TopDownProvider with.
		:return: A TopDownProvider instance.
		"""
		if image_provider_entity.type == "google_maps":
			return GoogleMapsProvider(image_provider_entity=self)
		if image_provider_entity.type == "mapbox":
			return MapboxProvider(image_provider_entity=self)
		if image_provider_entity.type == "ahn":
			return AhnProvider(image_provider_entity=self)
		raise ValueError("This image provider type is not defined")
