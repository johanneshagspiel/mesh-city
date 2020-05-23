"""
A module containing the overlay creator
"""
import csv
import os
from pathlib import Path
from shutil import copyfile

from PIL import Image, ImageDraw


class OverlayCreator:
	"""
	Class responsible for creating and managing overlays associated with the different detection
	requests
	"""

	def __init__(self, application, main_screen):
		"""
		Initializes the overlay creator
		:param application: the global application context 
		:param main_screen: the main screen of the application
		"""
		self.application = application
		self.main_screen = main_screen
		# TODO needs to change when we change to another request
		self.overlay_overview = {}
		self.map_overlay_overview = {}

	def create_overlay(self, detection_algorithm, image_size):
		"""
		Creates one overlay from the results of a detection algorithm
		:param detection_algorithm: what kind of detection algorithm created the result
		:param image_size: the size of the image used by the detection algorithm
		:return: nothing (adds the overlay to the overlay dictionary and updates main screen
		"""
		if detection_algorithm == "trees":
			# TODO change image size depending on image size used for prediction
			tree_overlay = Image.new('RGBA', (image_size[0], image_size[1]), (255, 255, 255, 0))
			draw = ImageDraw.Draw(tree_overlay)

			# TODO change path when finalizing working with layers and detection
			temp_path = Path.joinpath(
				self.application.file_handler.folder_overview["active_layer_path"][0],
				"trees",
				"test.csv"
			)

			with open(temp_path, newline='') as csvfile:
				spamreader = csv.reader(csvfile, delimiter=',')
				temp_counter = 0
				for row in spamreader:
					if len(row) > 0 and temp_counter > 0:
						draw.rectangle(
							xy=((float(row[1]), float(row[2])), (float(row[3]), float(row[4]))),
							outline="red"
						)
					temp_counter += 1

			temp_path = Path.joinpath(
				self.application.file_handler.folder_overview["active_layer_path"][0],
				"trees",
				"overlay_tree.png"
			)
			tree_overlay.save(temp_path, format="png")
			self.overlay_overview["trees"] = (temp_path, (int(image_size[0]), int(image_size[1])))

	def create_map_overlay(self, detection_algorithm, image_size):
		"""
		Creates an overlay for a map based on the results of an detection_algorithm
		:param detection_algorithm: the detection_algorithm that created the results
		:param image_size: the image size used by the detection algorithm
		:return: nothing (an image is added to the overlay dictionary)
		"""

		if detection_algorithm == "trees":
			# TODO change image size depending on image size used for prediction
			tree_map_overlay = Image.new('RGBA', (image_size[0], image_size[1]), (255, 255, 255, 0))
			draw = ImageDraw.Draw(tree_map_overlay)

			# TODO change path when finalizing working with layers and detection
			temp_path = Path.joinpath(
				self.application.file_handler.folder_overview["active_layer_path"][0],
				"trees",
				"test.csv"
			)

			with open(temp_path, newline='') as csvfile:
				spamreader = csv.reader(csvfile, delimiter=',')
				temp_counter = 0
				for row in spamreader:
					if len(row) > 0 and temp_counter > 0:
						draw.rectangle(
							xy=((float(row[1]), float(row[2])), (float(row[3]), float(row[4]))),
							outline="green", fill="green"
						)
					temp_counter += 1

			temp_path = Path.joinpath(
				self.application.file_handler.folder_overview["active_layer_path"][0],
				"trees",
				"map_overlay_tree.png"
			)
			tree_map_overlay.save(temp_path, format="png")
			self.map_overlay_overview["trees"] = (temp_path, (int(image_size[0]), int(image_size[1])))

	def create_map_image(self, overlays):
		"""
		Creates a map image based on the previously created map overlays
		:param overlays: the overlays to use
		:return: nothing (a map is created in temp)
		"""
		base = Image.new('RGB', (600, 600), (255, 255, 255))
		base.putalpha(255)

		for element in overlays:
			temp_dic_element = self.map_overlay_overview[element]
			temp_path = temp_dic_element[0]

			to_overlay = Image.open(temp_path)
			resized_base = base.resize(
				(temp_dic_element[1][0], temp_dic_element[1][1]), Image.ANTIALIAS
			)
			resized_base.alpha_composite(to_overlay)

		temp_path = Path.joinpath(
				self.application.file_handler.folder_overview["temp_path"][0],"map")

		# pylint: disable=E1101
		if temp_path.exists() is False:
			os.makedirs(temp_path)

		resized_base.save(Path.joinpath(temp_path, "concat_image_map_overlay.png"))
		self.application.file_handler.change(
			"active_image_path", temp_path)
		self.main_screen.active_layers = overlays

	def create_composite_image(self, overlays):
		"""
		Creates a composite overlay from multiple layers
		:param overlays: which layers to use for the composite image
		:return: nothing (creates a composite image and updates the main screen with it)
		"""

		copyfile(
			next(
			self.application.file_handler.folder_overview["active_image_path"]
			[0].glob("concat_image_*")
			),
			Path.joinpath(
			self.application.file_handler.folder_overview["temp_path"][0], "concat_image_overlay.png"
			)
		)

		base = Image.open(
			Path.joinpath(
			self.application.file_handler.folder_overview["temp_path"][0], "concat_image_overlay.png"
			)
		)
		base.putalpha(255)

		for element in overlays:
			temp_dic_element = self.overlay_overview[element]
			temp_path = temp_dic_element[0]

			to_overlay = Image.open(temp_path)
			resized_base = base.resize(
				(temp_dic_element[1][0], temp_dic_element[1][1]), Image.ANTIALIAS
			)
			resized_base.alpha_composite(to_overlay)

		resized_base.save(
			Path.joinpath(
			self.application.file_handler.folder_overview["temp_path"][0], "concat_image_overlay.png"
			)
		)
		self.application.file_handler.change(
			"active_image_path", self.application.file_handler.folder_overview["temp_path"][0]
		)
		self.main_screen.active_layers = overlays
