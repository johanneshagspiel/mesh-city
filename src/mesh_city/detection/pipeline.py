from pathlib import Path

from mesh_city.detection.detection_providers.deep_forest import DeepForest
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
		if self.type == "trees":
			test = Image.new('RGBA', (self.main_screen.image_width, self.main_screen.image_height), (255, 255, 255, 0))
			draw = ImageDraw.Draw(test)
			temp_path = Path.joinpath(self.application.file_handler.folder_overview["active_layer_path"][0], "trees", "test.csv")

			with open(temp_path, newline='') as csvfile:
				spamreader = csv.reader(csvfile, delimiter=',')
				temp_counter = 0
				for row in spamreader:
					if len(row) > 0 and temp_counter > 0:
						print("hi")
						draw.rectangle(xy=(row[1], row[2], row[3], row[4]), fill=(0, 192, 192), outline=(255, 255, 255))
					temp_counter += 1

			test.save("test.png", format="png")
			return None
