"""
See :class:`.Usage`
"""


class Usage:
	"""
	Represents the current quota usage of the user.
	"""

	def __init__(self):
		self.usage = self.init()

	def init(self):
		"""
		Sets the quota usages to their initial values.
		:return: The usage object.
		"""
		return {
			"google_maps": {"static map": 0, "geo_coding": 0},
			"mapbox": {"static map": 0, "geo_coding": 0},
			"ahn": {"static map": 0, "geo_coding": 0},
		}  # yapf: disable
