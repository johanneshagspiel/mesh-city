"""
A module containing the overlay creator
"""
import csv
from pathlib import Path

from PIL import Image, ImageDraw

from mesh_city.detection.pipeline import DetectionType
from mesh_city.request.google_layer import GoogleLayer
from mesh_city.request.trees_layer import TreesLayer
from mesh_city.util.image_util import ImageUtil


class OverlayCreator:
	"""
	Class responsible for creating and managing overlays associated with the different detection
	requests
	"""

	def __init__(self, application, building_instructions):
		"""
		Initializes the overlay creator
		:param application: the global application context 
		:param main_screen: the main screen of the application
		"""
		self.application = application
		self.building_instructions = building_instructions

	def create_map_overlay(self, detection_algorithm, image_size, number, path):
		"""
		Creates an overlay for a map based on the results of an detection_algorithm
		:param detection_algorithm: the detection_algorithm that created the results
		:param image_size: the image size used by the detection algorithm
		:return: nothing (an image is added to the overlay dictionary)
		"""

		if detection_algorithm == DetectionType.TREES:
			# TODO change image size depending on image size used for prediction
			tree_map_overlay = Image.new('RGBA', (image_size[0], image_size[1]), (255, 255, 255, 0))
			draw = ImageDraw.Draw(tree_map_overlay)

			with open(path, newline='') as csvfile:
				spamreader = csv.reader(csvfile, delimiter=',')
				temp_counter = 0
				for row in spamreader:
					if len(row) > 0 and temp_counter > 0:
						draw.rectangle(
							xy=((float(row[1]), float(row[2])), (float(row[3]), float(row[4]))),
							outline="green",
							fill="green"
						)
					temp_counter += 1

			temp_name = "map_tile_" + str(number) + ".png"
			temp_path = Path.joinpath(
				self.application.file_handler.folder_overview["active_request_path"],
				"trees",
				"map",
				temp_name
			)

			tree_map_overlay.save(temp_path, format="png")

			self.building_instructions.instructions[detection_algorithm]["Map"][1].append(
				str(temp_path)
			)
