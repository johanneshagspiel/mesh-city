import csv
import shutil
from pathlib import Path
from mesh_city.util.geo_location_util import GeoLocationUtil
from mesh_city.logs.log_entities.detection_meta import DetectionMeta

class MetaCreator:

	def __init__(self, application, building_instructions):
		self.application = application
		self.building_instructions = building_instructions

	def create_information(self, detection_algorithm, image_size, number, path):

		temp_name = "meta_tile_" + str(number) + ".json"
		temp_to_store = Path.joinpath(self.application.file_handler.folder_overview["active_meta_path"], temp_name)

		to_store = DetectionMeta(path_to_store=temp_to_store)
		to_store.information = {"Amount" : 0,
		                        "Objects" : {}}

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
						area_image = length_image*height_image

						new_to_store = to_store.information["Objects"]
						new_to_store[object_count] = {"label" : label, "xmin" : xmin, "ymin" : ymin,
						                              "xmax" : xmax, "ymax" : ymax, "score" : score,
						                              "length_image" : length_image,
						                              "height_image" : height_image,
						                              "area_image" : area_image}
						to_store.information["Objects"] = new_to_store
						object_count += 1

					temp_counter += 1

			to_store.information["Amount"] = object_count

			self.application.log_manager.create_log(to_store)

			self.building_instructions.instructions[detection_algorithm]["Meta"][1].append(str(temp_to_store))

			#total_area_covered = image_size[0] * image_size[1] * GeoLocationUtil.calc_meters_per_px()

	def combine_information(self, detection_algorithm):

		temp_to_store = Path.joinpath(self.application.file_handler.folder_overview["temp_meta_path"], "concat_information.json")
		combined = DetectionMeta(path_to_store=temp_to_store)

		temp_amount = 0
		temp_object = {}
		temp_counter = 1

		for element in self.building_instructions.instructions["Trees"]["Meta"][1]:
			temp_log = self.application.log_manager.read_log(str(element), "information")
			temp_amount += temp_log.information["Amount"]

			for value in temp_log.information["Objects"].values():
				temp_object[temp_counter] = value
				temp_counter += 1

		combined.information["Amount"] = temp_amount
		combined.information["Objects"] = temp_object
		self.application.log_manager.create_log(combined)

		#shutil.copy(self.building_instructions.instructions["Trees"]["Meta"][1][0], temp_to_store)
