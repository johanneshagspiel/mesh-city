from mesh_city.detection.detection_providers.deep_forest import DeepForest
from mesh_city.util.overlay_creator import OverlayCreator

class Pipeline:

	def __init__(self, application, type, main_screen):
		self.application = application
		self.type = type
		self.main_screen = main_screen
		self.push_backward()

	def push_forward(self):
		if self.type == "trees":
			DeepForest(self.application).detect()
			self.push_backward()

	def push_backward(self):
		OverlayCreator(self.type)

