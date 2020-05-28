import csv
from pathlib import Path
from mesh_city.util.geo_location_util import GeoLocationUtil

class MetaCreator:

	def __init__(self, application, main_screen):
		self.application = application
		self.main_screen = main_screen

	def create_information(self, detection_algorithm, image_size):

		if detection_algorithm == "trees":
			temp_path = Path.joinpath(
				self.application.file_handler.folder_overview["active_layer_path"],
				"trees",
				"test.csv"
			)

			total_area_covered = image_size[0] * image_size[1] * GeoLocationUtil.calc_meters_per_px()

			with open(temp_path, newline='') as csvfile:
				spamreader = csv.reader(csvfile, delimiter=',')
				temp_counter = 0
				for row in spamreader:
					if len(row) > 0 and temp_counter > 0:

						return None
