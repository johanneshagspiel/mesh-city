"""
Module containing the deep_forest tree detection algorithm
"""
from deepforest import deepforest


class TreeDetector:
	"""
	The class deepforest which contains a preliminary method to detect trees on an image.
	"""

	def __init__(self, nn_weights_path) -> None:
		self.model = deepforest.deepforest(saved_model=nn_weights_path)

	def detect(self, path):
		"""
		Method used to detect trees from images.

		:param image_path: path where the image is stored from which to detect trees
		:return: numpy array with bounding box over where threes are
		"""
		return self.model.predict_tile(
			raster_path=path, return_plot=False, patch_size=512, patch_overlap=0.25
		)
