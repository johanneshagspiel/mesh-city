"""
See :class:`.GeoLocationUtil`
"""

import math

from pyproj import Transformer


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

	@staticmethod
	def calc_meters_per_px(latitude, zoom, image_resolution=256):
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
		return GeoLocationUtil.circumference_earth * math.cos(latitude * math.pi / 180) / map_width

	@staticmethod
	def calc_next_location_latitude(latitude, longitude, zoom, direction):
		"""
		Calculates the latitude of the next adjacent tile.

		:param latitude: The current latitude.
		:param longitude: The current longitude.
		:param zoom: The zoom level.
		:param direction: If true gives the next higher latitude, if false the next lower.
		:return: The next latitude.
		"""

		latitude, longitude = GeoLocationUtil.normalise_coordinates(latitude, longitude, zoom)
		x_cor_tile, y_cor_tile = GeoLocationUtil.degree_to_tile_value(latitude, longitude, zoom)
		if direction:
			new_y_cor = y_cor_tile - 0.99
		else:
			new_y_cor = y_cor_tile + 1.01
		# offset values by slightly more than 1, such that there is no rounding error ambiguity
		# about which tile the next coordinates belong to. Boundary values cause problems.
		if (
			x_cor_tile < 0 or
			new_y_cor < 0 or
			x_cor_tile > 2.0**(zoom - 1) or
			new_y_cor > 2.0**(zoom - 1)
		):  # yapf: disable
			raise ValueError(
				"The x and y input cannot exceed the boundaries of the world tile grid"
			)
		new_latitude, new_longitude = GeoLocationUtil.tile_value_to_degree(x_cor_tile, new_y_cor, zoom)
		test_x, test_y = GeoLocationUtil.degree_to_tile_value(new_latitude, new_longitude, zoom)  # pylint: disable=unused-variable
		if test_y in (y_cor_tile + 1, y_cor_tile - 1):
			return new_latitude
		raise ValueError("New y tile coordinate is incorrect")

	@staticmethod
	def calc_next_location_longitude(latitude, longitude, zoom, direction):
		"""
		Calculates the longitude of the next adjacent tile.

		:param latitude: The current latitude.
		:param longitude: The current longitude.
		:param zoom: The zoom level.
		:param direction: If true gives the next higher longitude, if false the next lower.
		:return: The next longitude.
		"""

		latitude, longitude = GeoLocationUtil.normalise_coordinates(latitude, longitude, zoom)
		x_cor_tile, y_cor_tile = GeoLocationUtil.degree_to_tile_value(latitude, longitude, zoom)
		if direction:
			new_x_cor = x_cor_tile + 1.01
		else:
			new_x_cor = x_cor_tile - 0.99
		# offset values by slightly more than 1, such that there is no rounding error ambiguity
		# about which tile the next coordinates belong to. Boundary values cause problems.
		if new_x_cor < 0 or y_cor_tile < 0 or new_x_cor > 2.0**(zoom -
			1) or y_cor_tile > 2.0**(zoom - 1):
			raise ValueError(
				"The x and y input cannot exceed the boundaries of the world tile grid"
			)
		new_latitude, new_longitude = GeoLocationUtil.tile_value_to_degree(new_x_cor, y_cor_tile, zoom)
		test_x, test_y = GeoLocationUtil.degree_to_tile_value(new_latitude, new_longitude, zoom)  # pylint: disable=unused-variable
		if test_x in (x_cor_tile + 1, x_cor_tile - 1):
			return new_longitude
		raise ValueError("New x tile coordinate is incorrect")

	@staticmethod
	def degree_to_tile_value(latitude, longitude, zoom):
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
		total_number_of_tiles = 2.0**(zoom - 1)
		# number of tiles in the world tile grid: -1 as the downloaded images
		# have twice the resolution of the grid tiles of Google Maps, Bing Maps, and OpenStreetMap.
		x_cor_tile = int((longitude + 180.0) / 360.0 * total_number_of_tiles)
		y_cor_tile = int(
			(1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * total_number_of_tiles
		)
		return x_cor_tile, y_cor_tile

	@staticmethod
	def tile_value_to_degree(x_cor_tile, y_cor_tile, zoom, get_centre=True):
		"""
		Based on the x and y coordinates of a certain tile in the world grid of a certain zoom level
		it returns the geographical coordinates of that point. The world grid start in the top left
		corner with coordinates (0, 0) and end in the bottom right corner with (2^zoom − 1,
		2^zoom − 1).

		:param x_cor_tile: The point's x coordinate on the world tile grid.
		:param y_cor_tile: The point's y coordinate on the world tile grid.
		:param zoom: The zoom level.
		:param get_centre: if True returns centre coordinates. If False this returns the NW-corner
		of the square. Use the function with x_tile + 1 and/or y_tile + 1 to get the other corners.
		With x_tile + 0.5 & y_tile + 0.5 it will return the center of the tile.
		:return: the geographical coordinates of the input point.
		"""

		if get_centre:
			x_cor_tile += 0.5
			y_cor_tile += 0.5
		total_number_of_tiles = 2.0**(zoom - 1)
		if x_cor_tile < 0 or y_cor_tile < 0 or x_cor_tile > total_number_of_tiles - 1 or y_cor_tile > total_number_of_tiles - 1:
			raise ValueError(
				"The x and y input cannot exceed the boundaries of the world tile grid"
			)
		longitude = x_cor_tile / total_number_of_tiles * 360.0 - 180.0
		lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y_cor_tile / total_number_of_tiles)))
		latitude = math.degrees(lat_rad)
		return latitude, longitude

	@staticmethod
	def normalise_coordinates(latitude, longitude, zoom):
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
		x_cor_tile, y_cor_tile = GeoLocationUtil.degree_to_tile_value(latitude, longitude, zoom)
		new_latitude, new_longitude = GeoLocationUtil.tile_value_to_degree(x_cor_tile, y_cor_tile, zoom)
		return new_latitude, new_longitude

	@staticmethod
	def get_top_left_bottom_right_coordinates(first_coordinate, second_coordinate):
		"""
		Helper method to normalise any two coordinate input into a box defined by its top left
		coordinate and bottom right coordinate.

		:param first_coordinate:
		:param second_coordinate:
		:return: a tuple with the two normalised coordinates
		"""

		if first_coordinate[0] < second_coordinate[0]:
			bottom_lat = first_coordinate[0]
			top_lat = second_coordinate[0]
		else:
			bottom_lat = second_coordinate[0]
			top_lat = first_coordinate[0]

		if first_coordinate[1] < second_coordinate[1]:
			left_long = first_coordinate[1]
			right_long = second_coordinate[1]
		else:
			left_long = second_coordinate[1]
			right_long = first_coordinate[1]

		if bottom_lat > top_lat or left_long > right_long:
			raise ValueError(
				"The bottom latitude should be smaller than the top and the left longitude should be"
				"smaller than the right longitude"
			)
		return (top_lat, left_long), (bottom_lat, right_long)

	@staticmethod
	def get_bottom_left_top_right_coordinates(first_coordinate, second_coordinate):
		"""
		Helper method to normalise any two coordinate input into a box defined by its bottom left
		coordinate and top right coordinate.

		:param first_coordinate:
		:param second_coordinate:
		:return: a tuple with the two normalised coordinates
		"""

		(top_lat, left_long), (bottom_lat,
			right_long) = GeoLocationUtil.get_top_left_bottom_right_coordinates(
			first_coordinate, second_coordinate
			)
		return (bottom_lat, left_long), (top_lat, right_long)

	@staticmethod
	def transform_coordinates_to_mercator(latitude, longitude):
		"""
		Transforms standard longitude and latitude coordinates from the WGS 84 (EPSG 4326) to
		Easting and Northing values in the Web Mercator projection (EPSG 3857). Sample input/output:
		(51.50809, -0.1285907) -> (-14314.651244750548, 6711665.883938471).

		:param latitude: The current latitude.
		:param longitude: The current longitude.
		:return: meters east of 0, meters north of 0
		"""

		transformer = Transformer.from_crs("epsg:4326", "epsg:3857")
		m_east_of_0, m_north_of_0 = transformer.transform(latitude, longitude)
		return m_east_of_0, m_north_of_0

	@staticmethod
	def calc_map_units_per_px_cor(latitude, longitude, image_width, image_height, zoom):
		"""
		Given the input in geographical coordinates, calculates number of map units per pixel for
		the Web Mercator projection (EPSG 3857).

		:param latitude: the centre latitude of the tile
		:param longitude: the centre longitude of the tile
		:param image_width: image width
		:param image_height: image height
		:param zoom: the zoom level
		:return: a tuple with number of map units per pixel in x direction and y direction
		"""

		x_cor_grid, y_cor_grid = GeoLocationUtil.degree_to_tile_value(latitude, longitude, zoom)
		return GeoLocationUtil.calc_map_units_per_px_grid(
			x_cor_grid, y_cor_grid, image_width, image_height, zoom
		)

	@staticmethod
	def calc_map_units_per_px_grid(x_cor_grid, y_cor_grid, image_width, image_height, zoom):
		"""
		Given the input in grid coordinates, calculates number of map units per pixel for
		the Web Mercator projection (EPSG 3857).

		:param x_cor_grid: the x coordinate of the tile in the world grid
		:param y_cor_grid: the y coordinate of the tile in the world grid
		:param image_width: image width
		:param image_height: image height
		:param zoom: the zoom level
		:return: a tuple with number of map units per pixel in x direction and y direction
		"""

		nw_x, nw_y = x_cor_grid, y_cor_grid
		ne_x, ne_y = nw_x + 1, nw_y
		sw_x, sw_y = nw_x, nw_y + 1

		nw_geo_x, nw_geo_y = GeoLocationUtil.tile_value_to_degree(nw_x, nw_y, zoom, get_centre=False)
		ne_geo_x, ne_geo_y = GeoLocationUtil.tile_value_to_degree(ne_x, ne_y, zoom, get_centre=False)
		sw_geo_x, sw_geo_y = GeoLocationUtil.tile_value_to_degree(sw_x, sw_y, zoom, get_centre=False)

		nw_geo_x, nw_geo_y = GeoLocationUtil.transform_coordinates_to_mercator(nw_geo_x, nw_geo_y)
		ne_geo_x, ne_geo_y = GeoLocationUtil.transform_coordinates_to_mercator(ne_geo_x, ne_geo_y)
		sw_geo_x, sw_geo_y = GeoLocationUtil.transform_coordinates_to_mercator(sw_geo_x, sw_geo_x)

		pixels_per_unit_x_direction = (ne_geo_x - nw_geo_x) / image_width
		pixels_per_unit_y_direction = (sw_geo_y - nw_geo_y) / image_height

		return pixels_per_unit_x_direction, pixels_per_unit_y_direction

	@staticmethod
	def pixel_to_geo_coor(
		image_grid_x,
		image_grid_y,
		xmin,
		ymin,
		xmax,
		ymax,
		image_width=1024,
		image_height=1024,
		zoom=20
	):
		"""
		Method that transforms the position of a bounding box on an image, into pixel corodinaetes
		and then into geographical coordinates
		:param image_grid_x: the x coordinate of the grid position (aka. the Northwest corner) of the
		image
		:param image_grid_y: the y coordinate of the grid position (aka. the Northwest corner) of the
		image
		:param xmin:
		:param ymin:
		:param xmax:
		:param ymax:
		:param image_width:
		:param image_height:
		:param zoom: the zoom level, regarding the zoom level of the tile corresponding to the image
		:return: a tuple (latitude, longitude) in geographical coordinates (EPSG:4326)
		"""
		px_x = xmin + ((xmax - xmin) / 2)
		px_y = ymin + ((ymax - ymin) / 2)

		image_grid_x_offset = px_x / image_width
		image_grid_y_offset = px_y / image_height

		image_grid_x += image_grid_x_offset
		image_grid_y += image_grid_y_offset

		return GeoLocationUtil.tile_value_to_degree(image_grid_x, image_grid_y, zoom, False)
