"""
See :class:`.Scenario`
"""

from geopandas import GeoDataFrame
from pandas import DataFrame

from mesh_city.request.entities.request import Request


class Scenario:
	"""
	A class storing modified dataframes created from detected features.
	"""

	def __init__(
		self, trees: DataFrame, cars: DataFrame, buildings: GeoDataFrame, request: Request
	) -> None:
		self.trees = trees
		self.cars = cars
		self.buildings = buildings
		self.request = request
