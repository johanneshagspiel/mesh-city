"""
A module that contains all the different kinds of log entries used in this project
"""

from abc import ABC, abstractmethod


class LogEntity(ABC):
	"""
	An abstract log entry class that every instance of a log entry needs to correspond to
	"""

	def __init__(self, path_to_store):
		"""
		The initialization method. Sets the path to store the log
		:param path_to_store: where to store the log
		"""
		self.path_to_store = path_to_store

	@abstractmethod
	def for_storage(self):
		"""
		Turns one log entry into a form that can be stored following a storage standard (i.e. csv or json)
		:param self: the object to be stored
		:return: the object in a storage standard compliant form
		"""

	@abstractmethod
	def load_storage(self, storage):
		"""
		Method to load a class from a stored file
		:param storage: the file
		:return: nothing (the fields of the class are initialized correctly)
		"""

	@abstractmethod
	def action(self, logs):
		"""
		Performs an action associated with this log i.e. adding a new entry to a log
		:param self: the log entry to be added to some larger log
		:param logs: the larger log entry to be added to
		:return: nothing
		"""
