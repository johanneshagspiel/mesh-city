"""
Module containing the deep_forest tree detection algorithm
"""
from deepforest import deepforest

class DeepForest:
	"""
	The class deepforest which contains a preliminary method to detect trees on an image.
	"""

	def __init__(self):

		self.model = deepforest.deepforest()
		self.model.use_release()

	def detect(self, image_path):
		return self.model.predict_image(image_path=image_path, return_plot=False)
