from pathlib import Path

from mesh_city.util.image_util import ImageUtil

class RequestCreator:

	def __init__(self, application):
		self.image_util = ImageUtil()
		self.file_handler = application.file_handler

	def follow_instructions(self, list_to_make, BuildingInstructionsRequest):

		temp_to_build = BuildingInstructionsRequest.instructions[list_to_make]
		iteration_amount = temp_to_build[0]
		temp_path = Path.joinpath(self.file_handler.folder_overview["temp_image_path"][0],
		                          "concat_image_normal.png")

		if iteration_amount == 0:
			result_image = ImageUtil.concat_images_list(self=self.image_util,image_list=temp_to_build[1])

		else:
			temp_list_images = []

			for number in range(1, len(temp_to_build)):
				temp_image = ImageUtil.concat_images_list(self=self.image_util,image_list=temp_to_build[number])
				temp_list_images.append(temp_image)

			result_image = ImageUtil.combine_images_list(self=self.image_util, image_list=temp_list_images, iteration_amount=iteration_amount)

		result_image.save(fp=temp_path, format="png")
		self.file_handler.change("active_image_path", self.file_handler.folder_overview["temp_image_path"][0])
