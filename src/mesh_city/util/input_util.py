"""

source = https://code-maven.com/slides/python-programming/is-number
author = Gabor Szabo
"""

class InputUtil:

	def __init__(self):
		pass

	@staticmethod
	def is_float(val):
		try:
			num = float(val)
		except ValueError:
			return False
		return True

	@staticmethod
	def is_google_api(val):
		if not val:
			return False
		if not val.startswith('AIza'):
			return False
		return True
