class PriceTable:

	def __init__(self):
		pass

	def price(self, map_provider, action, user_info):
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
