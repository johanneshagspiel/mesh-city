"""
A module defining an observable interface.
"""
from abc import ABC


class Observable(ABC):
	"""
	An interface that encapsulates observability. Uses a dictionary to encapsulate observable state.
	"""

	def __init__(self):
		self.observers = []
		self.observable_state = {}

	def attach_observer(self, observer):
		"""
		Attaches a observer to the request maker
		:param observer: the observer to attach
		:return: nothing
		"""
		self.observers.append(observer)

	def detach_observer(self, observer):
		"""
		Detaches a observer from the detection pipeline and gets rid of its gui
		:param observer: the observer to detach
		:return:
		"""
		observer.destroy()
		self.observers.remove(observer)

	def notify_observers(self):
		"""
		Notifies all observers about a change in the state of the detection pipeline
		:return:
		"""
		for observer in self.observers:
			observer.update(self)
