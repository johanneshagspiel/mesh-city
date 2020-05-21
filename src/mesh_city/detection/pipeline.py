from pathlib import Path

from mesh_city.detection.detection_providers.deep_forest import DeepForest
from mesh_city.util.image_util import ImageUtil
from shutil import copyfile
from PIL import Image, ImageDraw
import csv


class Pipeline:

	def __init__(self, application, type, main_screen):
		self.application = application
		self.type = type
		self.main_screen = main_screen
		self.push_backward()

	def push_forward(self):
		if self.type == "trees":
			DeepForest(self.application).detect()
			self.push_backward()

	def push_backward(self):

		copyfile(self.application.file_handler.folder_overview["active_image_path"][0],
		         Path.joinpath(self.application.file_handler.folder_overview["temp_path"][0],
		                       "concat_image_overlay.png"))

		if self.type == "trees":
			# TODO change image size depending on image size used for prediction
			tree_overlay = Image.new('RGBA', (600, 600), (255, 255, 255, 0))
			draw = ImageDraw.Draw(tree_overlay)

			# TODO change path when finalizing working with layers and detection
			temp_path = Path.joinpath(
				self.application.file_handler.folder_overview["active_layer_path"][0], "trees",
				"test.csv")

			with open(temp_path, newline='') as csvfile:
				spamreader = csv.reader(csvfile, delimiter=',')
				temp_counter = 0
				for row in spamreader:
					if len(row) > 0 and temp_counter > 0:
						draw.rectangle(
							xy=((float(row[1]), float(row[2])), (float(row[3]), float(row[4]))),
							outline="red")
					temp_counter += 1

			tree_overlay.save(Path.joinpath(self.application.file_handler.folder_overview["active_layer_path"][0], "trees", "tree_overlay.png"), format="png")

			base = Image.open(Path.joinpath(self.application.file_handler.folder_overview["temp_path"][0], "concat_image_overlay.png"))
			base.putalpha(255)
			resized_base = base.resize((600, 600), Image.ANTIALIAS)
			resized_base.alpha_composite(tree_overlay)
			resized_base.save(Path.joinpath(self.application.file_handler.folder_overview["temp_path"][0], "concat_image_overlay.png"))
			self.application.file_handler.change("active_tile_path", self.application.file_handler.folder_overview["temp_path"][0])
