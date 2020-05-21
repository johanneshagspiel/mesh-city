"""
See :func:`.calculate_action_price`
"""
import sys

from range_key_dict import RangeKeyDict

class PriceTableUtil:

	def __init__(self, image_provider_entity, action):
		self.image_provider_entity = image_provider_entity
		self.action = action

		self.price_table_dic ={
			"google_maps" : {
				"static_map" : RangeKeyDict({
					(0, 100000) : 0.002,
					(100001, 500000) : 0.0016,
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
					(0, 50000): 0,
					(50001, 500000): 0.001,
					(500001, 1000000) : 0.0008,
					(1000001, 5000000) : 0.0006,
					(5000001, sys.maxsize): "NAN"
				}),
				"geocoding": RangeKeyDict({
					(0, 100000): 0,
					(100001, 500000): 0.00075,
					(500001, 1000000) : 0.0006,
					(1000001, 5000000) : 0.00045,
					(5000001, sys.maxsize): "NAN"
			})
		}
	}

	def calculate_action_price(self):

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
