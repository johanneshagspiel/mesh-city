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
		x_cor_tile, y_cor_tile = self.degree_to_tile_value(latitude, longitude, zoom)
		if direction:
			new_y_cor = y_cor_tile - 0.99
		else:
			new_y_cor = y_cor_tile + 1.01
		# 	offset values by slightly more than 1, such that there is no rounding error ambiguity
		if x_cor_tile < 0 or new_y_cor < 0 or x_cor_tile > 2.0**(zoom -
			1) or new_y_cor > 2.0**(zoom - 1):
			raise ValueError(
				"The x and y input cannot exceed the boundaries of the world tile grid"
			)

		new_latitude, new_longitude = self.tile_value_to_degree(x_cor_tile, new_y_cor, zoom)
		test_x, test_y = self.degree_to_tile_value(new_latitude, new_longitude, zoom)  # pylint: disable=unused-variable

		if test_y in (y_cor_tile + 1, y_cor_tile - 1):
			return new_latitude
		raise ValueError("New y tile coordinate is incorrect")

	def calc_next_location_longitude(self, latitude, longitude, zoom, direction):
		"""
		Calculates the longitude of the next adjacent tile.
		:param latitude: The current latitude.
		:param longitude: The current longitude.
		:param zoom: The zoom level.
		:param direction: If true gives the next higher longitude, if false the next lower.
		:return: The next longitude.
		"""
		x_cor_tile, y_cor_tile = self.degree_to_tile_value(latitude, longitude, zoom)
		if direction:
			new_x_cor = x_cor_tile + 1.01
		else:
			new_x_cor = x_cor_tile - 0.99
		# 	offset values by slightly more than 1, such that there is no rounding error ambiguity
		if new_x_cor < 0 or y_cor_tile < 0 or new_x_cor > 2.0**(zoom -
			1) or y_cor_tile > 2.0**(zoom - 1):
			raise ValueError(
				"The x and y input cannot exceed the boundaries of the world tile grid"
			)

		new_latitude, new_longitude = self.tile_value_to_degree(new_x_cor, y_cor_tile, zoom)
		test_x, test_y = self.degree_to_tile_value(new_latitude, new_longitude, zoom)  # pylint: disable=unused-variable

		if test_x in (x_cor_tile + 1, x_cor_tile - 1):
			return new_longitude
		raise ValueError("New x tile coordinate is incorrect")

	def degree_to_tile_value(self, latitude, longitude, zoom):
		"""
		Based on a geographical coordinate it returns the number coordinates of the closest tile in
		the world-grid of a certain zoom level.
		:param latitude: The current latitude.
		:param longitude: The current longitude.
		:param zoom: The zoom level.
		:return: x and y coordinates of the nearest tile in the world tile grid of the specified
		zoom level. This returns the NW-corner of the square. Use the function with x_tile + 1 and/or
		y_tile + 1 to get the other corners. With x_tile + 0.5 & y_tile + 0.5 it will return the
		center of the tile.
		"""
		if latitude < -85 or longitude < -180 or latitude > 85 or longitude > 180:
			raise ValueError(
				"The latitude, longitude input cannot exceed the boundaries of the map"
			)
		lat_rad = math.radians(latitude)
		total_number_of_tiles = 2.0**(
			zoom - 1
		)  # number of tiles in the world tile grid: -1 as the downloaded images
		# have twice the resolution of the grid tiles of Google Maps, Bing Maps, and OpenStreetMap.
		x_cor_tile = int((longitude + 180.0) / 360.0 * total_number_of_tiles)
		y_cor_tile = int(
			(1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * total_number_of_tiles
		)
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
		total_number_of_tiles = 2.0**(zoom - 1)
		if x_cor_tile < 0 or y_cor_tile < 0 or x_cor_tile > total_number_of_tiles - 1 or y_cor_tile > total_number_of_tiles - 1:
			raise ValueError(
				"The x and y input cannot exceed the boundaries of the world tile grid"
			)
		longitude = x_cor_tile / total_number_of_tiles * 360.0 - 180.0
		lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y_cor_tile / total_number_of_tiles)))
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
			raise ValueError(
				"The latitude, longitude input cannot exceed the boundaries of the map"
			)
		x_cor_tile, y_cor_tile = self.degree_to_tile_value(latitude, longitude, zoom)
		new_latitude, new_longitude = self.tile_value_to_degree(x_cor_tile, y_cor_tile, zoom)
		return new_latitude, new_longitude
