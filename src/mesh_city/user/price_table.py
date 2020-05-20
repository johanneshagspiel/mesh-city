"""
See :func:`.calculate_action_price`
"""


def calculate_action_price(map_provider, action, user_info):
	"""
	Returns price to perform a given action.
	:param map_provider: The map provider the action is part of.
	:param action: The given action.
	:param user_info: The current quota usage.
	:return: The predicted price.
	"""

	if map_provider == "google_maps":
		if action == "static_map":
			if user_info.get_usage("google_maps", "static_map") < 100000:
				return 0.002
			if user_info.get_usage("google_maps", "static_map") < 500000:
				return 0.0016
		if action == "geocoding":
			if user_info.get_usage("google_maps", "geo_coding") < 100000:
				return 0.005
			if user_info.get_usage("google_maps", "geo_coding") < 500000:
				return 0.004
	if map_provider == "ahn":
		if action == "static_map":
			return 0
	if map_provider == "mapbox":
		if action == "static_map":
			if user_info.get_usage("mapbox", "static_map") < 50000:
				return 0
			if user_info.get_usage("mapbox", "static_map") < 500000:
				return 0.001
			if user_info.get_usage("mapbox", "static_map") < 1000000:
				return 0.0008
			if user_info.get_usage("mapbox", "static_map") < 5000000:
				return 0.0006
		if action == "geocoding":
			if user_info.get_usage("mapbox", "geocoding") < 100000:
				return 0
			if user_info.get_usage("mapbox", "geocoding") < 500000:
				return 0.00075
			if user_info.get_usage("mapbox", "geocoding") < 1000000:
				return 0.0006
			if user_info.get_usage("mapbox", "geocoding") < 5000000:
				return 0.00045
	raise ValueError("Invalid provider and/or action")
