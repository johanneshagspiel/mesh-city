"""
See :class:`.UserInfo`
"""


class UserInfo:
	"""
	This class is used to define user information,
	such as name, api key , quota and the initial time where the information were inputted.
	"""

	def __init__(self, name, api_key, quota, usage, year, month, day, hour, minute, second):
		# TODO: Replace separate time args with one timestamp object
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

	def get_usage(self, map_provider, action):
		"""
		Returns the usage quota of a certain map provider and request action for the current user.
		:param map_provider: The map provider.
		:param action: The request action.
		:return: The number of used requests.
		"""
		raise NotImplementedError()
