"""
Module which provides a simple factory to create different types of TopDownProvider's.
"""

import csv
import math
import os
from pathlib import Path

from geopy import distance

from mesh_city.imagery_provider.top_down_provider.ahn_provider import AhnProvider
from mesh_city.imagery_provider.top_down_provider.google_maps_provider import GoogleMapsProvider
from mesh_city.imagery_provider.top_down_provider.mapbox_provider import MapboxProvider
from mesh_city.util.geo_location_util import GeoLocationUtil
from mesh_city.util.image_util import ImageUtil


class TopDownProviderFactory:
	"""
	A class that is responsible for handling requests to different map providers. Based on
	coordinates of the user it calculates all the locations that need to be downloaded, downloads them
	stores them in tile system: 9 images together make up one tile. These 9 images are, after being downloaded,
	combined into one large image that is displayed on the map.
	:param user_info: information about the user
	:param quota_manager: quota manager associated with the user
	"""
	def get_top_down_provider(self,image_provider_entity):
		if image_provider_entity.type == "google_maps":
			return GoogleMapsProvider(image_provider_entity=self)
		if image_provider_entity.type == "mapbox":
			return MapboxProvider(image_provider_entity=self)
		if image_provider_entity.type == "ahn":
			return AhnProvider(image_provider_entity=self)
		else:
			raise ValueError("This image provider type is not defined")
