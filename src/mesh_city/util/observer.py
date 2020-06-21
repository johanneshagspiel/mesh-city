"""
The module for the observer class
"""
from abc import ABC, abstractmethod

# pylint: disable=W0104,W0107
from mesh_city.util.observable import Observable


class Observer(ABC):
	"""
	The abstract observer class upon which all the oher observers are based
	"""

	def __init__(self):
		"""
		The initialization method
		"""
		pass

	@abstractmethod
	def update(self, observable: Observable):
		"""
		What to do when the observable is updated
		:param observable: The observable that this observer is observing
		:return:
		"""
		None

	@abstractmethod
	def destroy(self):
		"""
		How to destroy oneself once the observee has detached the observer
		:return:
		"""
		None
