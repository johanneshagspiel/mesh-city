"""
A module that contains all the different kinds of log entries used in this project
"""
from abc import ABC, abstractmethod

class LogEntry(ABC):
	"""
	An abstract logentry class that every instance of a log entry needs to correspond to
	"""

	def __init__(self, path_to_store):
		"""
		The initialization method. Sets the path to store the log
		:param path_to_store: where to store the log
		"""
		self.path_to_store = path_to_store

		@abstractmethod
		def for_json(self):
			"""
			Turns one log entry into a form that can be stored as a json
			:param self: the object to be stored as a json
			:return: a json compliant string
			"""

		@abstractmethod
		def action(self, logs, type_action = None):
			"""
			Performs an action associated with this log i.e. adding a new entry to a log
			:param self: the log entry to be added to some larger log
			:param logs: the larger log entry to be added to
			:return: nothing
			"""
