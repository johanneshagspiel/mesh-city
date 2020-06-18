"""
See :class:`.Scenario`
"""

from geopandas import GeoDataFrame
from pandas import DataFrame


class Scenario:
	"""
	A class storing modified dataframes created from detected features.
	"""

	def __init__(
		self,
		trees: DataFrame,
		cars: DataFrame,
		buildings: GeoDataFrame
	) -> None:
		self.trees = trees
		self.cars = cars
		self.buildings = buildings
