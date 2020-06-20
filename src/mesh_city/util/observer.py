"""
The module for the observer class
"""
from abc import ABC, abstractmethod


# pylint: disable=W0104,W0107
class Observer(ABC):
	"""
	The abstract observer class upon which all the oher observers are based on
	"""

	def __init__(self):
		"""
		The initialization method
		"""
		pass

	@abstractmethod
	def update(self, observee):
		"""
		What to do when the observee is updated
		:param observee: the subject to observ
		:return:
		"""
		None

	@abstractmethod
	def update_gui(self):
		"""
		How to update the gui
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
