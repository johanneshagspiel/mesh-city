"""
The module containing the request creator
"""
from pathlib import Path
from shutil import copyfile

from PIL import Image

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
		self.application = application
		self.image_util = ImageUtil()
		self.file_handler = application.file_handler

	# pylint: disable= W0108
	def follow_create_instructions(self, list_to_make, building_instructions_request):
		"""
		Method to create and load an image based on a list of images to load
		:param list_to_make: which images to create
		:param building_instructions_request: the file where the building instructions can be found
		:return: nothing (mainscreen shows a new image)
		"""

		if list_to_make[0] == "Google Maps":
			temp_to_build = building_instructions_request.instructions[list_to_make[0]]
			iteration_amount = temp_to_build[0]

			temp_path = Path.joinpath(self.file_handler.folder_overview["temp_image_path"],
			                          "concat_image_normal.png")

			if iteration_amount == 0:
				result_image = ImageUtil.concat_images_tile(self=self.image_util, image_list=temp_to_build[1])

			else:
				temp_list_images = []

				for number in range(1, len(temp_to_build)):
					temp_image = ImageUtil.concat_images_tile(self=self.image_util, image_list=temp_to_build[number])
					temp_list_images.append(temp_image)

				result_image = ImageUtil.combine_images_list(self=self.image_util, image_list=temp_list_images, iteration_amount=iteration_amount)

			result_image.save(fp=temp_path, format="png")
			self.file_handler.change("active_image_path", self.file_handler.folder_overview["temp_image_path"])

		if list_to_make[0] == "Trees":
			temp_to_build = building_instructions_request.instructions[list_to_make[0]][list_to_make[1]]
			iteration_amount = temp_to_build[0]

			temp_path = Path.joinpath(self.file_handler.folder_overview["temp_overlay_path"],
			                          "combined_image_overlay.png")

			if iteration_amount == 0:
				result_image = Image.open(temp_to_build[1][0])

			else:
				temp_list = list(map(lambda x : Image.open(x), temp_to_build[1]))
				result_image = ImageUtil.combine_images_list(self=self.image_util,
				                                             image_list=temp_list,
				                                             iteration_amount=iteration_amount)


			result_image.save(fp=temp_path, format="png")
			self.file_handler.change("active_image_path",
			                         self.file_handler.folder_overview["temp_overlay_path"])

	def follow_move_instructions(self, to_move, building_instructions_request, path_to_move):
		"""
		Method to move all the files stored in the path list to another folder
		:param to_move: which feature to move
		:param building_instructions_request: from which building_instructions_request move something
		:param path_to_move: where to move something to
		:return: nothing (all the files are moved)
		"""
		temp_to_move = building_instructions_request.instructions[to_move]

		for outer_counter in range(1, len(temp_to_move)):
			for number in range(0, len(temp_to_move[outer_counter])):
				file_name_to_move = Path(temp_to_move[outer_counter][number]).name
				new_path = Path.joinpath(path_to_move, file_name_to_move)
				copyfile(temp_to_move[outer_counter][number], new_path)

	def create_overlay_image(self, building_instructions_request, overlays, image_size):
		"""
		Creates a composite overlay from multiple layers
		:param overlays: which layers to use for the composite image
		:return: nothing (creates a composite image and updates the main screen with it)
		"""

		base = Image.open(next(self.application.file_handler.folder_overview["active_image_path"].glob("concat_image_*")))
		base.putalpha(255)

		self.follow_create_instructions([overlays[0], "Overlay"], building_instructions_request)

		to_overlay = Image.open(Path.joinpath(self.file_handler.folder_overview["temp_overlay_path"],
			                          "combined_image_overlay.png"))

		resized_overlay= to_overlay.resize((image_size[0], image_size[1]), Image.ANTIALIAS)
		resized_base = base.resize((image_size[0], image_size[1]), Image.ANTIALIAS)
		resized_base.alpha_composite(resized_overlay)

		resized_base.save(
			Path.joinpath(
			self.application.file_handler.folder_overview["temp_overlay_path"], "concat_image_overlay.png"
			)
		)
		self.application.file_handler.change(
			"active_image_path", self.application.file_handler.folder_overview["temp_overlay_path"]
		)

	# pylint: disable= E0602

	def create_map_image(self, overlays):
		"""
		Creates a map image based on the previously created map overlays
		:param overlays: the overlays to use
		:return: nothing (a map is created in temp)
		"""
		base = Image.new('RGB', (600, 600), (255, 255, 255))
		base.putalpha(255)

		for element in overlays:
			# pylint: disable = E1101
			temp_dic_element = self.map_overlay_overview[element]
			temp_path = temp_dic_element[0]

			to_overlay = Image.open(temp_path)
			resized_base = base.resize(
				(temp_dic_element[1][0], temp_dic_element[1][1]), Image.ANTIALIAS
			)
			resized_base.alpha_composite(to_overlay)

		temp_path = Path.joinpath(
				self.application.file_handler.folder_overview["temp_path"],"map")

		# pylint: disable=E1101
		if temp_path.exists() is False:
			os.makedirs(temp_path)

		resized_base.save(Path.joinpath(temp_path, "concat_image_map_overlay.png"))
		self.application.file_handler.change(
			"active_image_path", temp_path)

