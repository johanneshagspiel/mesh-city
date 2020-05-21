from pathlib import Path
from shutil import copyfile
from PIL import Image, ImageDraw
import csv

class OverlayCreator:

	def __init__(self):
		pass

	def create_overlay(self, type):
		if type == "trees":
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

	def create_composite_image(self, overlays):
		copyfile(next(self.application.file_handler.folder_overview["active_image_path"][0].glob(
			"concat_image_*")),
		         Path.joinpath(self.application.file_handler.folder_overview["temp_path"][0],
		                       "concat_image_overlay.png"))

		base = Image.open(
			Path.joinpath(self.application.file_handler.folder_overview["temp_path"][0],
			              "concat_image_overlay.png"))
		base.putalpha(255)

		for element in overlays:

		# TODO change size depending on size of overlay
		resized_base = base.resize((600, 600), Image.ANTIALIAS)
		resized_base.alpha_composite(tree_overlay)
		resized_base.save(
			Path.joinpath(self.application.file_handler.folder_overview["temp_path"][0],
			              "concat_image_overlay.png"))

		self.application.file_handler.change("active_image_path",
		                                     self.application.file_handler.folder_overview[
			                                     "temp_path"][0])
		self.main_screen.layer_active = "trees"
