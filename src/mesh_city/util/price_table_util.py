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
		previous_result = []
		print(previous_usage)
		print(previous_usage + additional_usage)

		for number in range(previous_usage, previous_usage + additional_usage):
			if api_name not in PriceTableUtil.price_table_dic:
				raise ValueError("The pricing for this API is not defined")
			if service_type not in PriceTableUtil.price_table_dic[api_name]:
				raise ValueError("The pricing for this API service is not defined")
			temp_result = PriceTableUtil.price_table_dic[api_name][service_type].get(number, -1)
			if temp_result == -1:
				print("-1")
				return [-1].extend(previous_result)
			cost += temp_result
			if cost >= monthly_quota and number != previous_usage + additional_usage:
				return [-1].extend(previous_result)

			previous_result = [cost, previous_usage + additional_usage - number]

		if (previous_usage + additional_usage) == 0:
			print("hi")
			return [0]

		return previous_result

	@staticmethod
	def one_increase(current_usage):
		"""
		calculates the price of one increase
		:return: the cost of one increase
		"""
		# TODO change if we ever support multiple map providers or actions
		return PriceTableUtil.price_table_dic["Google Maps"]["static_map"][current_usage+1]
