import os
from pathlib import Path


class DeepForest:

	def __init__(self, application):
		self.application = application

	def detect(self):
		os.makedirs(Path.joinpath(self.application.file_handler.folder_overview["active_layer_path"][0], "trees"))
		self.application.file_handler.change("selected_layer_path",
		                                     Path.joinpath(self.application.file_handler.folder_overview["active_layer_path"][0], "trees"))

		os.rename(Path.joinpath(self.application.file_handler.folder_overview["temp_path"][0], "test.csv"),
		          Path.joinpath(self.application.file_handler.folder_overview["selected_layer_path"][0], "test.csv"))
