from mesh_city.util.logs.log_entry.log_entry import LogEntry
from datetime import datetime
from calendar import monthrange

class ImageProviderLog(LogEntry):

	def __init__(self, path_to_store, name, api_key, quota):
		self.path_to_store = path_to_store
		self.name = name
		self.api_key = api_key
		self.date_reset = self.calculate_end_this_month()
		self.quota = quota

	def for_json(self):
		return {
			self.name : {
			"api_key" : self.api_key,
			"usage" : {
				"static_map" : 0,
				"geocoding" : 0,
				"total" : 0
			},
			"quota" : self.quota,
			"date_reset" : self.date_reset
			}
		}

	def action(self, logs):
		return self.for_json()

	def calculate_end_this_month(self):
		month = datetime.month
		year = datetime.year
		temp_end = monthrange(year, month)
		return str(temp_end[1]) + "/" + str(month) + "/" + str(year)

