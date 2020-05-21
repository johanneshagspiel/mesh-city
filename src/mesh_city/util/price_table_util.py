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


		# for entry in self.action:
		# 	for image in range(1, entry):
		# 		if self.image_provider_entity.type == "google_maps":
		# 			if entry[0] == "static_map":
		# 				if self.image_provider_entity.usage["static_map"] < 100000:
		# 					return 0.002
		# 				if self.image_provider_entity.usage["static_map"] < 500000:
		# 					return 0.0016
		# 			if entry[0] == "geocoding":
		# 				if self.image_provider_entity.usage["geocoding"] < 100000:
		# 					return 0.005
		# 				if self.image_provider_entity.usage["geocoding"] < 500000:
		# 					return 0.004
		# 		if self.image_provider_entity.type == "ahn":
		# 			if entry[0] == "static_map":
		# 				return 0
		# 		if self.image_provider_entity.type == "mapbox":
		# 			if entry[0] == "static_map":
		# 				if self.image_provider_entity.usage["static_map"] < 50000:
		# 					return 0
		# 				if self.image_provider_entity.usage["static_map"] < 500000:
		# 					return 0.001
		# 				if self.image_provider_entity.usage["static_map"] < 1000000:
		# 					return 0.0008
		# 				if self.image_provider_entity.usage["static_map"] < 5000000:
		# 					return 0.0006
		# 			if entry[0] == "geocoding":
		# 				if self.image_provider_entity.usage["geocoding"] < 100000:
		# 					return 0
		# 				if self.image_provider_entity.usage["geocoding"] < 500000:
		# 					return 0.00075
		# 				if self.image_provider_entity.usage["geocoding"] < 1000000:
		# 					return 0.0006
		# 				if self.image_provider_entity.usage["geocoding"] < 5000000:
		# 					return 0.00045
		# 		raise ValueError("Invalid provider and/or action")
		# return cost
