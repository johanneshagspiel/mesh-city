"""
A module containing the pipeline class which is responsible for moving images to the appropriate
detection algorithm in a form and frequency that they require and then moving the results to the
appropriate classes to create useful information in the form of overlays.
"""
import os
from pathlib import Path

from PIL import Image

from mesh_city.detection.detection_providers.deep_forest import DeepForest
from mesh_city.detection.overlay_creator import OverlayCreator
from mesh_city.util.image_util import ImageUtil


class Pipeline:
	"""
	A class responsible for moving data to the detection algorithm in a way they like and then
	routing the results to the appropriate classes to create useful information.
	"""

	def __init__(self, application, main_screen, type_of_detection, building_instructions):
		"""
		The initialization method.
		:param application: the global application context
		:param type_of_detection: where to send the images to i.e. to detect trees
		:param main_screen: the main screen of the application
		"""
		self.application = application
		self.type_of_detection = type_of_detection
		self.main_screen = main_screen
		self.building_instructions = building_instructions

		self.image_util = ImageUtil()

		self.temp_path = None

	def push_forward(self):
		"""
		Moving the images to the appropriate detection algorithm in the required format
		:return:nothing
		"""
		for element in self.type_of_detection:
			if element == "Trees":
				deep_forest = DeepForest()
				self.temp_path = Path.joinpath(self.application.file_handler.folder_overview["active_request_path"], "trees")
				os.makedirs(self.temp_path)
				temp_path_2 = Path.joinpath(self.temp_path, "raw_data")
				os.makedirs(temp_path_2)
				self.application.file_handler.change("active_raw_data_path", temp_path_2)

				for tile_number in range(1, len(self.building_instructions.instructions["Google Maps"])):
					temp_tile_image = self.image_util.concat_images_list(image_list=self.building_instructions.instructions["Google Maps"][tile_number])
					temp_path_2 = Path.joinpath(self.application.file_handler.folder_overview["temp_detection_path"], "temp_image.png")
					temp_tile_image.resize((600, 600), Image.ANTIALIAS).save(fp=temp_path_2, format="png")
					result = deep_forest.detect(temp_path_2.absolute().as_posix())

					temp_name = "raw_data_tile_" + str(tile_number) + ".csv"
					temp_path_3 = Path.joinpath(self.application.file_handler.folder_overview["active_raw_data_path"], temp_name)

					with open(temp_path_3, "w") as to_store:
						result.to_csv(to_store)
						to_store.close()

				self.push_backward((600, 600), element)

	def push_backward(self, image_size, type_detection):
		"""
		Moving the results from the detection algorithm to the sink classes
		:param image_size: the image size used by the detection algorithm
		:return: nothing (but it updates the image on the main_screen with a composite overlay image)
		"""

		temp_overlay_path = Path.joinpath(self.temp_path, "overlay")
		os.makedirs(temp_overlay_path)
		temp_map_path = Path.joinpath(self.temp_path, "map")
		os.makedirs(temp_map_path)

		overlay_creator = OverlayCreator(self.application, self.building_instructions)

		counter = 1

		for file in self.application.file_handler.folder_overview["active_raw_data_path"].glob('*'):
			if file.is_file():
				self.main_screen.overlay_creator.create_overlay(
					detection_algorithm=type_detection, image_size=(image_size[0], image_size[1]),
					number=counter, path=file
				)
				self.main_screen.overlay_creator.create_map_overlay(
					detection_algorithm=type_detection, image_size=(image_size[0], image_size[1]),
					number=counter, path=file
				)
				# self.main_screen.meta_creator.create_information(
				# 	detection_algorithm=type_detection, image_size=(image_size[0], image_size[1])
				# )
				counter += 1

		# self.main_screen.overlay_creator.create_composite_image(["trees"])

