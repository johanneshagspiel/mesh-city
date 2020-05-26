"""
Entry module of the application.
"""

from mesh_city.application import Application
from mesh_city.imagery_provider import request_manager
from mesh_city.util import geo_location_util
from mesh_city.util.geo_location_util import GeoLocationUtil


def main() -> None:
	"""
	Entry function of the application.
	:return: Nothing.
	"""
	# Application()
	coordinates = (50, 5)

	geo_location_util = GeoLocationUtil()
	x_tile, y_tile = geo_location_util.degree_to_tile_value(49.99979502712741, 5.000152587890625, 20)
	print(x_tile, y_tile)

	normalised_latitude, normalised_longitude = geo_location_util.normalise_coordinates(50, 5, 20)
	x, y = geo_location_util.degree_to_tile_value(normalised_latitude, normalised_longitude, 20)
	print(normalised_latitude, normalised_longitude)
	print(x, y)

	top_latitude = geo_location_util.calc_next_location_latitude(50, 5, 20, True)
	bottom_latitude = geo_location_util.calc_next_location_latitude(50, 5, 20, False)
	right_long = geo_location_util.calc_next_location_longitude(50, 5, 20, True)
	left_long = geo_location_util.calc_next_location_longitude(50, 5, 20, False)

	print(top_latitude, bottom_latitude, right_long, left_long)

	top_x, top_y = geo_location_util.degree_to_tile_value(top_latitude, normalised_longitude, 20)
	bottom_x, bottom_y = geo_location_util.degree_to_tile_value(bottom_latitude, normalised_longitude, 20)
	right_x, right_y = geo_location_util.degree_to_tile_value(normalised_latitude, right_long, 20)
	left_x, left_y = geo_location_util.degree_to_tile_value(normalised_latitude, left_long, 20)

	print(top_x, top_y)
	print(bottom_x, bottom_y)
	print(right_x, right_y)
	print(left_x, left_y)


	grid_position = geo_location_util.degree_to_tile_value(90, 181, 20)
	print(grid_position)

	normalised_coordinates1 = geo_location_util.normalise_coordinates(50, 5, 20)
	print(normalised_coordinates1)

	normalised_coordinates = geo_location_util.tile_value_to_degree(grid_position[0], grid_position[1], 20)
	normalised_grid_position = geo_location_util.degree_to_tile_value(normalised_coordinates[0], normalised_coordinates[1], 20)
	print(normalised_coordinates)
	print(normalised_grid_position)

	grid_position_plus1 = normalised_grid_position[0] + 2, normalised_grid_position[1]
	coordinates_plus1 = geo_location_util.tile_value_to_degree(grid_position_plus1[0], grid_position_plus1[1], 20)
	print(coordinates_plus1)
	print(grid_position_plus1)




if __name__ == '__main__':
	main()
