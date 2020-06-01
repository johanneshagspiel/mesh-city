"""
A module of the detection meta class
"""
from mesh_city.logs.log_entities.log_entity import LogEntity

class DetectionMeta(LogEntity):
	"""
	The log entity that stores meta information
	"""

	def __init__(self, path_to_store, json=None):
		super().__init__(path_to_store=path_to_store)
		if json is None:
			self.information ={}
		else:
			self.information = {}
			self.load_json(json)

	def action(self, logs):
		"""
		What to do when log manager calls write log
		:param logs:
		:return:
		"""
		return self.for_json()

	def load_json(self, list_from_csv):
		"""
		How to load the class from json
		:param json: the json file from which to log the class from
		:return: nothing (the fields are all set correctly)
		"""
		temp_object = {}
		object_count = 1
		for row in list_from_csv:
			if len(row) > 1:
				object_count += 1
				temp_object[object_count] = {"label" : row[0], "xmin" :  row[1], "ymin" :  row[2],
							                              "xmax" :  row[3], "ymax" :  row[4],
							                                "score" :  row[5],
							                              "length_image" :  row[6],
							                              "height_image" :  row[7],
							                              "area_image" :  row[8]}

		self.information["Amount"] = object_count - 1
		self.information["Objects"] = temp_object


	def for_json(self):
		return self.information

	def for_csv(self):
		"""
		Turns the class into a csv compliant form
		:return: the class in csv compliant form
		"""
		temp_list_overall = []
		temp_list = []

		temp_list_overall.append(["label", "xmin", "ymin","xmax", "ymax", "score",
		                  "length_image", "height_image","area_image"])

		for object in self.information["Objects"].values():
			for element in object.values():
				temp_list.append(element)
			temp_list_overall.append(temp_list)
			temp_list = []

		return temp_list_overall


