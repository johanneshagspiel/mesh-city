"""
A module containing the pipeline class which is responsible for moving images to the appropriate
detection algorithm in a form and frequency that they require and then moving the results to the
appropriate classes to create useful information in the form of overlays.
"""

import os

from PIL import Image

from mesh_city.detection.detection_providers.building_detector import BuildingDetector
from mesh_city.detection.detection_providers.deep_forest import DeepForest
from mesh_city.detection.meta_data_creator import MetaDataCreator
from mesh_city.detection.overlay_creator import OverlayCreator
from mesh_city.detection.raster_vector_converter import RasterVectorConverter
from mesh_city.imagery_provider.request_creator import RequestCreator
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
		self.main_screen = main_screen
		self.type_of_detection = type_of_detection
		self.building_instructions = building_instructions

		self.image_util = ImageUtil()
		self.request_creator = RequestCreator(self.application)
		self.temp_path = None
		self.building_detector = None

	# pylint: disable=E1101
	def push_forward(self) -> None:
		"""
		Moving the images to the appropriate detection algorithm in the required format
		:return: nothing
		"""

		for element in self.type_of_detection:
			if element == "Trees":
				deep_forest = DeepForest()

				self.temp_path = self.application.file_handler.folder_overview["active_request_path"].joinpath("trees")
				os.makedirs(self.temp_path)

				req_raw_data_path = self.temp_path.joinpath("raw_data")
				os.makedirs(req_raw_data_path)
				self.application.file_handler.change("active_raw_data_path", req_raw_data_path)

				for tile_number in range(1, len(self.building_instructions.instructions["Google Maps"]["Paths"])):
					combined_image = self.image_util.concat_images_tile(
						image_list=self.building_instructions.instructions["Google Maps"]["Paths"][tile_number]
					)
					combined_image_path = self.application.file_handler.folder_overview["temp_detection_path"].joinpath("temp_image.png")
					combined_image.resize((600, 600), Image.ANTIALIAS).save(fp=combined_image_path, format="png")
					result = deep_forest.detect(image_path=combined_image_path)

					raw_data_csv_filename = "raw_data_tile_" + str(tile_number) + ".csv"
					raw_data_csv_path = self.application.file_handler.folder_overview["active_raw_data_path"].joinpath(raw_data_csv_filename)

					with open(raw_data_csv_path, "w") as to_store:
						result.to_csv(to_store)

				# TODO all the request creator methods for making one large image have to change
				self.push_backward(image_size=(600, 600), detection_type=element)

			elif element == "Buildings":
				if self.building_detector is None:
					self.building_detector = BuildingDetector(self.application.file_handler)

				self.temp_path = self.application.file_handler.folder_overview["active_request_path"].joinpath("buildings")
				self.temp_path.mkdir()

				combined_image = self.image_util.concat_images_tile(
					image_list=self.building_instructions.instructions["Google Maps"]["Paths"][1])
				combined_image_path = self.application.file_handler.folder_overview["temp_detection_path"].joinpath("temp_image.png")
				combined_image.resize((512, 512), Image.ANTIALIAS).save(fp=combined_image_path, format="png")

				result = self.building_detector.detect(image_path=combined_image_path)

				result_path = self.temp_path.joinpath("raster_mask.png")
				result.save(result_path)

				r2v = RasterVectorConverter()
				polygons = r2v.mask_to_vector(detection_mask=result_path)
				bounding_boxes = r2v.vector_to_bounding_boxes(polygons=polygons)

				raw_data_csv_path = self.temp_path.joinpath("raw_data_tile_0.csv")

				with open(raw_data_csv_path, "w") as csv_file:
					csv_file.write("number,xmin,ymin,xmax,ymax\n")
					for index, ((y_min, x_min), (y_max, x_max)) in enumerate(bounding_boxes):
						csv_file.write("%d,%f,%f,%f,%f\n" % (index, x_min, y_min, x_max, y_max))

				self.push_backward(image_size=(512, 512), detection_type=element)

	def push_backward(self, image_size: (int, int), detection_type: str) -> None:
		"""
		Moving the results from the detection algorithm to the sink classes
		:param image_size: the image size used by the detection algorithm
		:return: nothing (but it updates the image on the main_screen with a composite overlay image)
		"""

		temp_overlay_path = self.temp_path.joinpath("overlay")
		os.makedirs(temp_overlay_path)
		self.application.file_handler.change("active_overlay_path", temp_overlay_path)

		temp_map_path = self.temp_path.joinpath("map")
		os.makedirs(temp_map_path)
		self.application.file_handler.change("active_map_path", temp_map_path)

		temp_meta_path = self.temp_path.joinpath("meta")
		os.makedirs(temp_meta_path)
		self.application.file_handler.change("active_meta_path", temp_meta_path)

		temp_overlay_creator = OverlayCreator(self.application, self.building_instructions)
		temp_meta_data_creator = MetaDataCreator(self.application, self.building_instructions)

		counter = 1

		self.building_instructions.instructions[detection_type] = {"Overlay": [0, []]}
		temp_entry = self.building_instructions.instructions[detection_type]
		temp_entry["Map"] = [0, []]
		temp_entry["Meta"] = [0, []]
		self.building_instructions.instructions[detection_type] = temp_entry

		for file in self.application.file_handler.folder_overview["active_raw_data_path"].glob("*"):
			if file.is_file():
				temp_overlay_creator.create_overlay(
					detection_algorithm=detection_type,
					image_size=(image_size[0], image_size[1]),
					number=counter,
					path=file,
				)
				temp_overlay_creator.create_map_overlay(
					detection_algorithm=detection_type,
					image_size=(image_size[0], image_size[1]),
					number=counter,
					path=file,
				)
				temp_meta_data_creator.create_information(
					detection_algorithm=detection_type,
					image_size=(image_size[0], image_size[1]),
					number=counter,
					path=file,
				)
				counter += 1

		temp_len = len(self.building_instructions.instructions[detection_type]["Overlay"][1])
		temp_len = temp_len / 2
		if temp_len == 0.5:
			temp_len = 0
		self.building_instructions.instructions[detection_type]["Overlay"][0] = temp_len
		self.building_instructions.instructions[detection_type]["Map"][0] = temp_len

		self.application.log_manager.write_log(self.building_instructions)

		self.request_creator.create_overlay_image(
			self.building_instructions, self.type_of_detection, (600, 600)
		)
		temp_meta_data_creator.combine_information(self.type_of_detection)
