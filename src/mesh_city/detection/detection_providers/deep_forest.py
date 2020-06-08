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

	def detect(self, image):
		"""
		Method used to detect trees from images
		:param image_path: path where the image is stored from which to detect trees
		:return: numpy array with bounding box over where threes are
		"""
		return self.model.predict_image(numpy_image=image, return_plot=False)
