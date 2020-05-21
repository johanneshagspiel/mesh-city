from mesh_city.detection.detection_providers.deep_forest import DeepForest
from mesh_city.util.overlay_creator import OverlayCreator


class Pipeline:

	def __init__(self, application, type, main_screen):
		self.application = application
		self.type = type
		self.main_screen = main_screen
		self.push_backward((600, 600))

	def push_forward(self):
		if self.type == "trees":
			DeepForest(self.application).detect()
			self.push_backward((600, 600))

	def push_backward(self, image_size):
		self.main_screen.overlay_creator.create_overlay(
			type=self.type, image_size=(image_size[0], image_size[1])
		)
		self.main_screen.overlay_creator.create_composite_image(["trees"])
