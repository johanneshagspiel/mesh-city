"""
See :class:`.GeoLocationUtil`
"""

import math


class GeoLocationUtil:

	def __init__(self):
		pass
	"""
	Collection of functions related to converting geographical units.
	"""

	def calc_meters_per_px(self, latitude, zoom):
		"""
		Method which calculates the number of meters one pixel at this specific latitude and zoom level
		represents.
		:param latitude: respective latitude.
		:param zoom: respective zoom level, accepts a value between 1 and 21. Urban areas have higher
		zoom levels, whilst Antarctica has a max zoom level of 16.
		:return: the number of meters one pixel represents in an image.
		"""
		return 156543.03392 * math.cos(latitude * math.pi / 180) / math.pow(2, zoom)

	def calc_next_location_latitude(self, latitude, zoom, image_size_x, direction):
		"""
		Calculates the latitude of the next request.
		:param latitude: The current latitude.
		:param zoom: The zoom level.
		:param image_size_x: The width of the tile in pixels.
		:param direction: If true gives the next higher latitude, if false the next lower.
		:return: The next latitude.
		"""
		meters_per_px = self.calc_meters_per_px(latitude, zoom)
		next_center_distance_meters = meters_per_px * image_size_x
		if direction:
			new_latitude = latitude + (
				(next_center_distance_meters / 6378137) * (180 / math.pi)
			)
			new_latitude = latitude + ((next_center_distance_meters / 6378137) * (180 / math.pi))
		else:
			new_latitude = latitude - (
				(next_center_distance_meters / 6378137) * (180 / math.pi)
			)
			new_latitude = latitude - ((next_center_distance_meters / 6378137) * (180 / math.pi))
		return new_latitude

	def calc_next_location_longitude(self, latitude, longitude, zoom, image_size_y, direction):
		"""
		Calculates the longitude of the next request.
		:param latitude: The current latitude.
		:param longitude: The current longitude.
		:param zoom: The zoom level.
		:param image_size_y: The height of the tile in pixels.
		:param direction: If true gives the next higher longitude, if false the next lower.
		:return: The next longitude.
		"""
		meters_per_px = self.calc_meters_per_px(latitude, zoom)
		next_center_distance_meters = meters_per_px * image_size_y
		if direction:
			new_longitude = longitude + (
				(next_center_distance_meters / 6378137) *
				(180 / math.pi) / math.cos(latitude * math.pi / 180)
			)
		else:
			new_longitude = longitude - (
				(next_center_distance_meters / 6378137) *
				(180 / math.pi) / math.cos(latitude * math.pi / 180)
			)
		return new_longitude

