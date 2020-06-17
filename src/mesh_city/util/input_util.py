"""
See :class:`.InputUtil`
source = https://code-maven.com/slides/python-programming/is-number
author = Gabor Szabo
"""


class InputUtil:
	"""
	A utility class for doing simple input checks
	"""

	def __init__(self):
		pass

	@staticmethod
	def is_float(val: str) -> bool:
		"""
		Tries to cast a string to a float
		:param val: A string
		:return: A bool indicating whether it represents a valid float.
		"""
		try:
			float(val)
		except ValueError:
			return False
		return True

	@staticmethod
	def is_google_api(val: str) -> bool:
		"""
		Checks if a string can be a valid Google Maps api key.
		:param val: A string
		:return: A bool indicating whether the string can be a valid api key.
		"""
		if not val:
			return False
		if not val.startswith('AIza'):
			return False
		return True
