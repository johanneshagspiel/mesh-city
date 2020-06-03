# pylint: disable=W0611, W0613
"""
A module containing the meta creator class
"""
import csv
from pathlib import Path

from mesh_city.logs.log_entities.detection_meta_data import DetectionMetaData
from mesh_city.util.geo_location_util import GeoLocationUtil


class MetaDataCreator:
	"""
	Class that stores meta information from the results of the detection algorithms
	"""

	def __init__(self, application, building_instructions):
		self.application = application
		self.building_instructions = building_instructions

	def create_information(self, detection_algorithm, image_size, number, path):
		"""
		Turns the result of an detection algorithm into information
		:param detection_algorithm: the detection algorithm that created results
		:param image_size: the size of the image on which the detection was run
		:param number: the number of the tile
		:param path: the path where to read the detection algorithm results from
		:return: nothing (creates a new log with all the information from the detection algorithm)
		"""

		temp_name = "meta_tile_" + str(number) + ".csv"
		temp_to_store = Path.joinpath(
			self.application.file_handler.folder_overview["active_meta_path"], temp_name
		)

		to_store = DetectionMetaData(path_to_store=temp_to_store)
		to_store.information = {"Amount": 0, "Objects": {}}

		if detection_algorithm == "Trees":

			with open(path, newline='') as csvfile:
				spamreader = csv.reader(csvfile, delimiter=',')
				temp_counter = 0
				object_count = 1
				for row in spamreader:
					if len(row) > 0 and temp_counter > 0:
						xmin = (float(row[1]))
						ymin = (float(row[2]))
						xmax = (float(row[3]))
						ymax = (float(row[4]))
						score = (float(row[5]))
						label = str(row[6])
						length_image = xmax - xmin
						height_image = ymax - ymin
						area_image = length_image * height_image

						new_to_store = to_store.information["Objects"]
						new_to_store[object_count] = {
							"label": label,
							"xmin": xmin,
							"ymin": ymin,
							"xmax": xmax,
							"ymax": ymax,
							"score": score,
							"length_image": length_image,
							"height_image": height_image,
							"area_image": area_image
						}
						to_store.information["Objects"] = new_to_store
						object_count += 1

					temp_counter += 1

			to_store.information["Amount"] = object_count

			self.application.log_manager.create_log(to_store, "csv")

			self.building_instructions.instructions[detection_algorithm]["Meta"][1].append(
				str(temp_to_store)
			)

			#total_area_covered = image_size[0] * image_size[1] * GeoLocationUtil.calc_meters_per_px()

	def combine_information(self, detection_algorithm):
		"""
		Method to combine meta information from multiple tiles into one
		:param detection_algorithm: the detection algorithm used to create the results
		:return: nothing (created a log combining the information from the different tiles)
		"""

		temp_to_store = Path.joinpath(
			self.application.file_handler.folder_overview["temp_meta_path"], "concat_information.csv"
		)
		combined = DetectionMetaData(path_to_store=temp_to_store)

		temp_amount = 0
		temp_object = {}
		temp_counter = 1

		for algorithm in detection_algorithm:
			if algorithm == "Trees":
				for element in self.building_instructions.instructions["Trees"]["Meta"][1]:
					temp_log = self.application.log_manager.read_log(str(element), "information")
					temp_amount += temp_log.information["Amount"]

					for value in temp_log.information["Objects"].values():
						temp_object[temp_counter] = value
						temp_counter += 1

		combined.information["Amount"] = temp_amount
		combined.information["Objects"] = temp_object

		self.application.log_manager.create_log(combined, "csv")
