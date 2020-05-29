"""
The module containing the request creator
"""
from pathlib import Path

from mesh_city.util.image_util import ImageUtil


class RequestCreator:
	"""
	The class creating the image seen on the main screen based on a list of images to be combined
	"""

	def __init__(self, application):
		"""
		The initialization method
		:param application: The global application context
		"""
		self.image_util = ImageUtil()
		self.file_handler = application.file_handler

	def follow_instructions(self, list_to_make, building_instructions_request):
		"""
		Method to create and load an image based on a list of images to load
		:param list_to_make: which images to create
		:param building_instructions_request: the file where the building instructions can be found
		:return: nothing (mainscreen shows a new image)
		"""

		temp_to_build = building_instructions_request.instructions[list_to_make]
		iteration_amount = temp_to_build[0]
		temp_path = Path.joinpath(
			self.file_handler.folder_overview["temp_image_path"], "concat_image_normal.png"
		)

		if iteration_amount == 0:
			result_image = ImageUtil.concat_images_list(
				self=self.image_util, image_list=temp_to_build[1]
			)

		else:
			temp_list_images = []

			for number in range(1, len(temp_to_build)):
				temp_image = ImageUtil.concat_images_list(
					self=self.image_util, image_list=temp_to_build[number]
				)
				temp_list_images.append(temp_image)

			result_image = ImageUtil.combine_images_list(
				self=self.image_util, image_list=temp_list_images, iteration_amount=iteration_amount
			)

		result_image.save(fp=temp_path, format="png")
		self.file_handler.change(
			"active_image_path", self.file_handler.folder_overview["temp_image_path"]
		)
