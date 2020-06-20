"""
This module defines
"""


class WidgetGeometry:
	"""
	A WidgetGeometry struct for storing positional information about widgets.
	"""

	def __init__(self, width: int, height: int, x_position: int, y_position: int):
		assert width > 0
		assert height > 0

		self.width: int = width
		self.height: int = height
		self.x_position: int = x_position
		self.y_position: int = y_position
