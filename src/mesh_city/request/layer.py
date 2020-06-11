"""
See :class:`.Layer`
"""

from abc import ABC


class Layer(ABC):
	"""
	An abstract base class that request layers inherit from.
	"""

	def __init__(self, width: int, height: int) -> None:
		self.width = width
		self.height = height
