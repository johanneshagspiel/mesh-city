"""
A module containing the overlay creator
"""
import csv
import os
from pathlib import Path
import random
import copy

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
		temp_path = Path.joinpath(self.application.file_handler.folder_overview["temp_image_path"],
		                          "concat_image_normal.png")
		# TODO needs to change when we change tree detection size
		temp_image = Image.open(temp_path).resize((600, 600), Image.ANTIALIAS)

		images_to_add = []
		images_to_add.append(temp_image)
		object_counter= detection_info.information["Amount"]

		for tree in range(0, trees_to_add):
			tree_to_duplicate = detection_info.information["Objects"][random.randint(1, detection_info.information["Amount"])]
			location_to_place_it_to = detection_info.information["Objects"][random.randint(1, detection_info.information["Amount"])]
			image_to_paste = temp_image.crop(box=(float(tree_to_duplicate["xmin"]),
			                                      float(tree_to_duplicate["ymin"]),
			                                      float(tree_to_duplicate["xmax"]),
			                                      float(tree_to_duplicate["ymax"])))

			temp_entry = self.calculate_new_location(tree_to_duplicate, location_to_place_it_to)
			detection_info.information["Objects"][object_counter] = temp_entry
			object_counter += 1

			where_to_place = ((int(float(temp_entry["xmin"])), int(float(temp_entry["ymax"]))))

			temp_image.paste(image_to_paste, box=where_to_place)
			temp_to_add_image = copy.deepcopy(temp_image)
			images_to_add.append(temp_to_add_image)

		temp_path_directory = Path.joinpath(self.application.file_handler.folder_overview["active_request_path"], "more_trees")
		number_generated = 1

		if "Generated" not in building_instructions.instructions.keys():
			building_instructions.instructions["Generated"] = {}

		if "More Trees" not in building_instructions.instructions["Generated"]:
			temp_dic_entry = building_instructions.instructions["Generated"]
			temp_dic_entry["More Trees"] =  [0, []]
			building_instructions.instructions["Generated"] = temp_dic_entry
			os.makedirs(temp_path_directory)
		else:
			number_generated = len(building_instructions.instructions["Generated"]["More Trees" ][1]) + 1

		temp_name = "concat_image_trees_" + str(number_generated) + ".gif"
		temp_path_file = Path.joinpath(temp_path_directory, temp_name)

		images_to_add[0].save(temp_path_file,
		               save_all=True, append_images=images_to_add[1:], optimize=False, duration=100, loop=0)

		temp_to_store = building_instructions.instructions["Generated"]["More Trees"][1]
		temp_to_store_addition = str(temp_path_file)
		temp_to_store.append(temp_to_store_addition)

		building_instructions.instructions["Generated"]["More Trees"][1] = temp_to_store
		self.application.log_manager.write_log(building_instructions)

		self.application.file_handler.change("active_image_path", temp_path_directory)

	def calculate_new_location(self,what_to_place, where_to_place):
		old_xmin = what_to_place["xmin"]
		old_ymax = what_to_place["ymax"]
		old_xmax = what_to_place["xmax"]
		old_ymin = what_to_place["ymin"]

		new_xmin = str(float(old_xmin) + 5)
		new_ymax = str(float(old_ymax) + 5)
		new_xmax = str(float(old_xmax) + 5)
		new_ymin = str(float(old_ymin) + 5)

		new_entry = {"label" : what_to_place["label"], "xmin" :  new_xmin, "ymin" :  new_ymin,
		             "xmax" :  new_xmax, "ymax" :  new_ymax, "score" : what_to_place["score"],
					 "length_image" :  what_to_place["length_image"],
                     "height_image" : what_to_place["height_image"],
                     "area_image" :  what_to_place["area_image"]}

		return new_entry
