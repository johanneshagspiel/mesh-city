class UserInfo:

	def __init__(self, name, api_key, quota, usage, year, month, day, hour, minute, second):
		self.name = name
		self.api_key = api_key
		self.quota = quota
		self.usage = usage
		self.year = year
		self.month = month
		self.day = day
		self.hour = hour
		self.minute = minute
		self.second = second

		def get_usage(map_provider, action):
			return 0


class Usage:

	def __init__(self):
		self.usage = self.start()

	def start(self):
		return {
			"google_maps": {
			"static map": 0, "geo_coding": 0
			},
			"mapbox": {
			"static map": 0, "geo_coding": 0
			},
			"ahn": {
			"static map": 0, "geo_coding": 0
			}
		}
