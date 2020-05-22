"""
See :class:`.GeoLocationUtil`
"""

import math


class GeoLocationUtil:
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

	def calc_next_location_latitude(self, latitude, longitude, zoom, direction):
		"""
		Calculates the latitude of the next adjacent tile.
		:param latitude: The current latitude.
		:param longitude: The current longitude.
		:param zoom: The zoom level.
		:param direction: If true gives the next higher latitude, if false the next lower.
		:return: The next latitude.
		"""
		normalised_latitude, normalised_longitude = self.normalise_coordinates(latitude, longitude, zoom)
		x_cor_tile, y_cor_tile = self.degree_to_tile_value(normalised_latitude, normalised_longitude, zoom)
		if direction:
			y_cor_tile = y_cor_tile - 2
		else:
			y_cor_tile = y_cor_tile + 2
		if x_cor_tile < 0 or y_cor_tile < 0 or x_cor_tile > 2.0 ** zoom or y_cor_tile > 2.0 ** zoom:
			raise ValueError("The x and y input cannot exceed the boundaries of the world tile grid")
		new_latitude, new_longitude = self.tile_value_to_degree(x_cor_tile, y_cor_tile, zoom)
		return new_latitude

	def calc_next_location_longitude(self, latitude, longitude, zoom, direction):
		"""
		Calculates the longitude of the next adjacent tile.
		:param latitude: The current latitude.
		:param longitude: The current longitude.
		:param zoom: The zoom level.
		:param direction: If true gives the next higher longitude, if false the next lower.
		:return: The next longitude.
		"""
		normalised_latitude, normalised_longitude = self.normalise_coordinates(latitude, longitude, zoom)
		x_cor_tile, y_cor_tile = self.degree_to_tile_value(normalised_latitude, normalised_longitude, zoom)
		if direction:
			x_cor_tile = x_cor_tile + 2
		else:
			x_cor_tile = x_cor_tile - 2
		if x_cor_tile < 0 or y_cor_tile < 0 or x_cor_tile > 2.0 ** zoom or y_cor_tile > 2.0 ** zoom:
			raise ValueError("The x and y input cannot exceed the boundaries of the world tile grid")
		new_latitude, new_longitude = self.tile_value_to_degree(x_cor_tile, y_cor_tile, zoom)
		return new_longitude

	def degree_to_tile_value(self, latitude, longitude, zoom):
		"""
		Based on a geographical coordinate it returns the number coordinates of the closest tile in
		the world-grid of a certain zoom level.
		:param latitude: The current latitude.
		:param longitude: The current longitude.
		:param zoom: The zoom level.
		:return: x and y coordinates of the nearest tile in the world tile grid of the specified
		zoom level.
		"""
		if latitude < -85 or longitude < -180 or latitude > 85 or longitude > 180:
			raise ValueError("The latitude, longitude input cannot exceed the boundaries of the map")
		lat_rad = math.radians(latitude)
		n = 2.0 ** zoom
		x_cor_tile = int((longitude + 180.0) / 360.0 * n)
		y_cor_tile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
		# normalises x and y tile coordinates to always be on uneven positions, such that requested
		# images, which are two tiles apart, can never half overlap.
		if x_cor_tile % 2 == 0:
			x_cor_tile = x_cor_tile - 1
		if y_cor_tile % 2 == 0:
			y_cor_tile = y_cor_tile - 1
		return x_cor_tile, y_cor_tile

	def tile_value_to_degree(self, x_cor_tile, y_cor_tile, zoom):
		"""
		Based on the x and y coordinates of a certain tile in the world grid of a certain zoom level
		it returns the geographical coordinates of that point. The world grid start in the top left
		corner with coordinates (0, 0) and end in the bottom right corner with (2^zoom − 1,
		2^zoom − 1)
		:param x_cor_tile: The point's x coordinate on the world tile grid.
		:param y_cor_tile: The point's y coordinate on the world tile grid.
		:param zoom: The zoom level.
		:return: the geographical coordinates of the input point.
		"""
		n = 2.0 ** zoom
		if x_cor_tile < 0 or y_cor_tile < 0 or x_cor_tile > n - 1 or y_cor_tile > n - 1:
			raise ValueError("The x and y input cannot exceed the boundaries of the world tile grid")
		longitude = x_cor_tile / n * 360.0 - 180.0
		lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y_cor_tile / n)))
		latitude = math.degrees(lat_rad)
		return latitude, longitude

	def normalise_coordinates(self, latitude, longitude, zoom):
		"""
		Method that normalises any geographical coordinates input to the most nearby geographical
		coordinates of a point on the world tile grid of that zoom level.
		:param latitude: The current latitude.
		:param longitude: The current longitude.
		:param zoom: The zoom level.
		:return: x and y coordinates of the nearest tile in the world grid of the specified zoom
		level.
		"""
		if latitude < -85 or longitude < -180 or latitude > 85 or longitude > 180:
			raise ValueError("The latitude, longitude input cannot exceed the boundaries of the map")
		x_cor_tile, y_cor_tile = self.degree_to_tile_value(latitude, longitude, zoom)
		new_latitude, new_longitude = self.tile_value_to_degree(x_cor_tile, y_cor_tile, zoom)
		return new_latitude, new_longitude

