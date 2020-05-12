import math
from pathlib import Path

import requests

from mesh_city.imagery_provider.top_down_provider.top_down_provider import TopDownProvider


class AhnProvider(TopDownProvider):
	color_to_height = {
		(12, 52, 124): -7.5,
		(12, 68, 132): -6.5,
		(12, 84, 132): -5.5,
		(12, 92, 132): -4.5,
		(20, 108, 140): -3.5,
		(28, 116, 140): -2.75,
		(20, 132, 140): -2.25,
		(28, 148, 148): -1.75,
		(36, 148, 148): -1.25,
		(36, 156, 140): -0.75,
		(20, 164, 132): -0.25,
		(28, 172, 124): 0.25,
		(28, 180, 108): 0.75,
		(20, 188, 100): 1.25,
		(20, 188, 84): 1.75,
		(12, 196, 68): 2.25,
		(4, 204, 52): 3,  # 2.5-3, 3-3.5
		(4, 220, 4): 4,  # 3.5-4, 4-4.5
		(44, 228, 4): 4.75,
		(68, 228, 4): 5.5,
		(100, 236, 4): 6.5,
		(124, 236, 4): 7.5,
		(148, 244, 4): 8.5,
		(180, 244, 4): 9.5,
		(204, 244, 4): 11,
		(236, 252, 4): 13,
		(252, 252, 4): 15,
		(252, 244, 4): 17,
		(252, 228, 4): 19,
		(244, 212, 4): 25,  # 20-25, 25-30
		(252, 196, 12): 32.5,
		(244, 188, 4): 37.5,
		(244, 180, 20): 42.5,
		(244, 164, 20): 47.5,
		(236, 164, 20): 55,
		(244, 156, 20): 65,
		(228, 140, 28): 75,
		(228, 132, 36): 85,
		(220, 124, 36): 95,
		(212, 108, 44): 125,  # 100-125, 125-150
		(204, 100, 52): 162.5,
		(204, 92, 52): 187.5,
		(196, 84, 60): 250,  # 200-250, 250-300
	}  # yapf: disable

	def __init__(self, user_info, quota_manager):
		TopDownProvider.__init__(self, user_info=user_info, quota_manager=quota_manager)

	def get_and_store_location(self, x, y, name, new_folder_path):

		bounding_box_coordinates = self.calculate_bounding_box(x, y, 20, 640, 640)

		xmin = str(bounding_box_coordinates[0])
		ymin = str(bounding_box_coordinates[1])
		xmax = str(bounding_box_coordinates[2])
		ymax = str(bounding_box_coordinates[3])
		width = str(640)
		height = str(640)

		response = requests.get(
			"https://geodata.nationaalgeoregister.nl/ahn3/wms?request=GetMap&service=wms&CRS=EPSG:4326&bbox=%s,%s,%s,%s&width=%s&height=%s&layers=ahn3_05m_dsm&styles=ahn3:ahn3_05m_detail&format=image/png&version=1.30"
			% (xmin, ymin, xmax, ymax, width, height)
		)

		filename = name
		to_store = Path.joinpath(new_folder_path, filename)

		with open(to_store, "wb") as output:
			output.write(response.content)

	def calculate_bounding_box(self, x, y, zoom, image_size_x, image_size_y):
		right = self.calc_next_location_latitude(x, y, zoom, image_size_x / 2, True)
		left = self.calc_next_location_latitude(x, y, zoom, image_size_x / 2, False)
		up = self.calc_next_location_longitude(x, y, zoom, image_size_y / 2, True)
		down = self.calc_next_location_longitude(x, y, zoom, image_size_y / 2, False)

		self.check_in_netherlands(left, down)
		self.check_in_netherlands(right, up)

		return [left, down, right, up]

	def check_in_netherlands(self, x, y):
		if (
			x < 50.671799068129744 or
			x > 53.61086457823865 or
			y < 3.197334098049271 or
			y > 7.275203841667622
		):  # yapf: disable
			print("Height information is only available in the Netherlands - Sorry!")

	def calc_next_location_latitude(self, latitude, longitude, zoom, image_size_x, direction):
		meters_per_px = 156543.03392 * math.cos(latitude * math.pi / 180) / math.pow(2, zoom)
		next_center_distance_meters = meters_per_px * image_size_x
		if direction:
			new_latitude = latitude + (next_center_distance_meters / 6378137) * (180 / math.pi)
		else:
			new_latitude = latitude - (next_center_distance_meters / 6378137) * (180 / math.pi)
		return new_latitude

	def calc_next_location_longitude(self, latitude, longitude, zoom, image_size_y, direction):
		meters_per_px = 156543.03392 * math.cos(latitude * math.pi / 180) / math.pow(2, zoom)
		next_center_distance_meters = meters_per_px * image_size_y
		if direction:
			new_longitude = longitude + (next_center_distance_meters / 6378137) * (180 /
				math.pi) / math.cos(latitude * math.pi / 180)
		else:
			new_longitude = longitude - (next_center_distance_meters / 6378137) * (180 /
				math.pi) / math.cos(latitude * math.pi / 180)
		return new_longitude
