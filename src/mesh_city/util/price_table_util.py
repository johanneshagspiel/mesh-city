"""
Module containing price table util class
"""

from range_key_dict import RangeKeyDict


class QuotaException(Exception):
	"""
	A simple exception to signal that an action would exceed a set quota.
	"""


class PriceTableUtil:
	"""
	A utility class needed to calculate the costs of a request
	"""
	price_table_dic = {
		"Google Maps":
		{
		"static_map": RangeKeyDict({
		(0, 100001): 0.002, (100001, 500001): 0.0016,
		}),
		"geocoding": RangeKeyDict({
		(0, 100001): 0.005, (100001, 500001): 0.004,
		})
		},
		"Mapbox":
		{
		"static_map":
		RangeKeyDict(
		{
		(0, 50001): 0, (50001, 500001): 0.001, (500001, 1000001): 0.0008, (1000001, 5000001): 0.0006,
		}
		),
		"geocoding":
		RangeKeyDict(
		{
		(0, 100001): 0, (100001, 500001): 0.00075, (500001, 1000001): 0.0006, (1000001, 5000001):
		0.00045
		}
		)
		}
	}

	@staticmethod
	def calculate_action_price(
		api_name, service_type, previous_usage, additional_usage, monthly_quota
	):
		"""
		calculates the price of an action
		:return: the cost in list form (in case of error additional information)
		"""
		cost = 0
		for number in range(previous_usage, previous_usage + additional_usage):
			if api_name not in PriceTableUtil.price_table_dic:
				raise ValueError("The pricing for this API is not defined")
			if service_type not in PriceTableUtil.price_table_dic[api_name]:
				raise ValueError("The pricing for this API service is not defined")
			temp_result = PriceTableUtil.price_table_dic[api_name][service_type].get(number, -1)
			if temp_result == -1:
				raise ValueError("The price for the given requests is not defined.")
			cost += temp_result
			if number >= monthly_quota and number != previous_usage + additional_usage:
				raise QuotaException("These requests would exceed the quota.")
		return cost
