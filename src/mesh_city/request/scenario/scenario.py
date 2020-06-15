"""
See :class:`.Scenario`
"""

from abc import ABC


class Scenario(ABC):
	"""
	An abstract base class that request scenarios inherit from.
	"""

	def __init__(self, width: int, height: int) -> None:
		self.width = width
		self.height = height
