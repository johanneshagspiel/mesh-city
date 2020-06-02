"""
A module containing the overlay creator
"""
import csv
from pathlib import Path
import random

from PIL import Image, ImageDraw


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

	def create_overlay(self, detection_algorithm, image_size, number, path):
		"""
		Creates one overlay from the results of a detection algorithm
		:param detection_algorithm: what kind of detection algorithm created the result
		:param image_size: the size of the image used by the detection algorithm
		:return: nothing (adds the overlay to the overlay dictionary and updates main screen
		"""

		if detection_algorithm == "Trees":
			# TODO change image size depending on image size used for prediction
			tree_overlay = Image.new('RGBA', (image_size[0], image_size[1]), (255, 255, 255, 0))
			draw = ImageDraw.Draw(tree_overlay)

			with open(path, newline='') as csvfile:
				spamreader = csv.reader(csvfile, delimiter=',')
				temp_counter = 0
				for row in spamreader:
					if len(row) > 0 and temp_counter > 0:
						draw.rectangle(
							xy=((float(row[1]), float(row[2])), (float(row[3]), float(row[4]))),
							outline="red"
						)
					temp_counter += 1

			temp_name = "overlay_tile_" + str(number) + ".png"
			temp_path = Path.joinpath(self.application.file_handler.folder_overview["active_request_path"], "trees", "overlay", temp_name)

			tree_overlay.save(temp_path, format="png")

			self.building_instructions.instructions[detection_algorithm]["Overlay"][1].append(str(temp_path))

	def create_map_overlay(self, detection_algorithm, image_size, number, path):
		"""
		Creates an overlay for a map based on the results of an detection_algorithm
		:param detection_algorithm: the detection_algorithm that created the results
		:param image_size: the image size used by the detection algorithm
		:return: nothing (an image is added to the overlay dictionary)
		"""

		if detection_algorithm == "Trees":
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
							outline="green", fill="green"
						)
					temp_counter += 1

			temp_name = "map_tile_" + str(number) + ".png"
			temp_path = Path.joinpath(self.application.file_handler.folder_overview["active_request_path"], "trees", "map", temp_name)

			tree_map_overlay.save(temp_path, format="png")

			self.building_instructions.instructions[detection_algorithm]["Map"][1].append(str(temp_path))

	def create_image_with_more_trees(self, trees_to_add, detection_info, building_instructions):
		for tree in range(0, trees_to_add):
			tree_to_duplicate = detection_info.information["Objects"][random.randint(1, detection_info.information["Amount"])]
			tree_to_place_it_to = detection_info.information["Objects"][random.randint(1, detection_info.information["Amount"])]
