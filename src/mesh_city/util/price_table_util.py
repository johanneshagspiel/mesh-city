"""
Module containing price table util class
"""
import sys
from range_key_dict import RangeKeyDict

class PriceTableUtil:
	"""
	A utility class needed to calculate the costs of a request
	"""

	def __init__(self, image_provider_entity, action):
		"""
		Sets up a price table dictionary to check how much a request costs
		:param image_provider_entity: the image provider entity making the request
		:param action: what kind of request it is
		"""
		self.image_provider_entity = image_provider_entity
		self.action = action

		self.price_table_dic ={
			"google_maps" : {
				"static_map" : RangeKeyDict({
					(0, 100001) : 0.002,
					(100001, 500001) : 0.0016,
					(500001, sys.maxsize) : "NAN"
				}),
				"geocoding" : RangeKeyDict({
					(0, 100001) : 0.005,
					(100001, 500001) : 0.004,
					(500001, sys.maxsize): "NAN"
				})
			},
			"mapbox" : {
				"static_map": RangeKeyDict({
					(0, 50001): 0,
					(50001, 500001): 0.001,
					(500001, 1000001) : 0.0008,
					(1000001, 5000001) : 0.0006,
					(5000001, sys.maxsize): "NAN"
				}),
				"geocoding": RangeKeyDict({
					(0, 100000): 0,
					(100001, 500001): 0.00075,
					(500001, 1000001) : 0.0006,
					(1000001, 5000001) : 0.00045,
					(5000001, sys.maxsize): "NAN"
			})
		}
	}

	def calculate_action_price(self):
		"""
		calculates the price of an action
		:return: the cost in list form (in case of error additional information)
		"""
		cost = 0
		temp_type = self.image_provider_entity.type
		for entry in self.action:
			action_type = entry[0]
			for number in range(self.image_provider_entity.usage[action_type], self.image_provider_entity.usage[action_type]+entry[1]):
				temp_result = self.price_table_dic[temp_type][action_type][number]
				if temp_result == "NAN":
					return ["NAN", number, cost]
				cost += 1 * temp_result
				if cost >= self.image_provider_entity.quota and number != self.image_provider_entity.usage[action_type]+entry[1]:
					return ["Quota", number, cost]
		return [cost]
