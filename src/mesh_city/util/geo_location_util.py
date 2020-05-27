"""
See :class:`.GeoLocationUtil`
"""

import math

# pylint: disable=W0105
class GeoLocationUtil:
	"""
	A helper class representing all the methods needed for calculations with geo lcoations
	"""

	def __init__(self):
		pass
	"""
	Collection of functions related to converting geographical units. Based on the following:
	Ground resolution = cos(latitude * pi/180) * earth circumference / map width.
	Earth circumference's at the Equator is 40075017 meters.
	Map width = map height = tile resolution * 2^level.
	The standard tile width/height is 256 pixels. As used in the quad-tree division of the mercator
	projection in Google Maps, Bing Maps, and OpenStreetMap.
	"""

	radius_earth = 6378137  # in meters.
	circumference_earth = 40075016.69  # in meters. calculated as: 2 pi * radius_earth
	standard_base_meters_per_px = 156543.03392  # calculated as: circumference_earth / 256

	def calc_meters_per_px(self, latitude, zoom, image_resolution=256):
		"""
		Method which calculates the number of meters one pixel at this specific latitude and zoom level
		represents.
		:param latitude: respective latitude.
		:param zoom: respective zoom level, accepts a value between 1 and 21. Urban areas have higher
		zoom levels, whilst Antarctica has a max zoom level of 16.
		:param image_resolution: the height and width in pixels of the tiles/images.
		:return: the number of meters one pixel represents in an image.
		"""
		map_width = math.pow(2, zoom) * image_resolution
		return self.circumference_earth * math.cos(latitude * math.pi / 180) / map_width

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
				(next_center_distance_meters / self.radius_earth) *
				(180 / math.pi) / math.cos(latitude * math.pi / 180)
			)
		else:
			new_longitude = longitude - (
				(next_center_distance_meters / self.radius_earth) *
				(180 / math.pi) / math.cos(latitude * math.pi / 180)
			)
		return new_longitude
