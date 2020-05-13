import math

class GeoLocationUtil:

	def __init__(self):
		pass

	def calc_meters_per_px(self, latitude, zoom):
		"""
		Method which calculates the number of meters one pixel at this specific latitude and zoom level
		represents.
		:param latitude: respective latitude.
		:param zoom: respective zoom level, accepts a value between 1 and 21. Urban areas have higher
		zoom levels, whilst Antarctica has a max zoom level of 16.
		:return: the number of meters one pixel represents in an image.
		"""
		return 156543.03392 * math.cos(latitude * math.pi / 180) / math.pow(2, zoom)

	def calc_next_location_latitude(self, latitude, longitude, zoom, image_size_x, direction, multiplier = 1):
		meters_per_px = self.calc_meters_per_px(latitude, zoom)
		next_center_distance_meters = meters_per_px * image_size_x
		if direction:
			new_latitude = latitude + (((next_center_distance_meters / 6378137) * (180 / math.pi)) * multiplier)
		else:
			new_latitude = latitude - (((next_center_distance_meters / 6378137) * (180 / math.pi)) * multiplier)
		return new_latitude

	def calc_next_location_longitude(self, latitude, longitude, zoom, image_size_y, direction, multiplier = 1):
		meters_per_px = self.calc_meters_per_px(latitude, zoom)
		next_center_distance_meters = meters_per_px * image_size_y
		if direction:
			new_longitude = longitude + (((next_center_distance_meters / 6378137) * (180 /
			                                                                       math.pi) / math.cos(
				latitude * math.pi / 180)) * multiplier)
		else:
			new_longitude = longitude - (((next_center_distance_meters / 6378137) * (180 /
			                                                                       math.pi) / math.cos(
				latitude * math.pi / 180)) * multiplier)
		return new_longitude
