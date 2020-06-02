"""
A module containing the pipeline class which is responsible for moving images to the appropriate
detection algorithm in a form and frequency that they require and then moving the results to the
appropriate classes to create useful information in the form of overlays.
"""
from mesh_city.detection.detection_providers.deep_forest import DeepForest


class Pipeline:
	"""
	A class responsible for moving data to the detection algorithm in a way they like and then
	routing the results to the appropriate classes to create useful information.
	"""

	def __init__(self, application, type_of_detection, main_screen):
		"""
		The initialization method.
		:param application: the global application context
		:param type_of_detection: where to send the images to i.e. to detect trees
		:param main_screen: the main screen of the application
		"""
		self.application = application
		self.type = type_of_detection
		self.main_screen = main_screen
		self.push_backward((600, 600))

	def push_forward(self):
		"""
		Moving the images to the appropriate detection algorithm in the required format
		:return:nothing
		"""
		if self.type == "trees":
			DeepForest(self.application).detect()
			self.push_backward((600, 600))

	def push_backward(self, image_size):
		"""
		Moving the results from the detection algorithm to the sink classes
		:param image_size: the image size used by the detection algorithm
		:return: nothing (but it updates the image on the main_screen with a composite overlay image)
		"""
		self.main_screen.overlay_creator.create_overlay(
			detection_algorithm=self.type, image_size=(image_size[0], image_size[1])
		)
		self.main_screen.overlay_creator.create_map_overlay(
			detection_algorithm=self.type, image_size=(image_size[0], image_size[1])
		)
		self.main_screen.overlay_creator.create_composite_image(["trees"])
