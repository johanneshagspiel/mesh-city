"""
Module containing the deep_forest tree detection algorithm
"""
import os
from pathlib import Path
from deepforest import deepforest


class DeepForest:
	"""
	The class deepforest which contains a preliminary method to detect treens on an image.
	"""

	def __init__(self, application):
		"""
		The initialization method that sets up a deep forest object
		:param application: the global application context
		"""
		self.application = application

	def detect(self):
		"""
		Preliminary detect function for early preview that moves a file created externally with deep_forest predictions to the appropriate location
		:return: nothing
		"""
		os.makedirs(
			Path.joinpath(
			self.application.file_handler.folder_overview["active_layer_path"], "trees"
			)
		)
		self.application.file_handler.change(
			"selected_layer_path",
			Path.joinpath(
			self.application.file_handler.folder_overview["active_layer_path"], "trees"
			)
		)

		os.rename(
			Path.joinpath(self.application.file_handler.folder_overview["temp_path"], "test.csv"),
			Path.joinpath(
			self.application.file_handler.folder_overview["selected_layer_path"], "test.csv"
			)
		)
