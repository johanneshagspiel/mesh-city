"""
The module containing the request creator
"""
from pathlib import Path
from shutil import copyfile

from PIL import Image

from mesh_city.request.google_layer import GoogleLayer
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

	def create_canvas_image_layer(self,width,height,layer):
		if isinstance(layer,GoogleLayer):
			tiles = layer.tiles
			images = []
			for tile in tiles:
				images.append(Image.open(self.file_handler.folder_overview["image_path"].joinpath(tile.path)))
			concat_image = ImageUtil.concat_image_grid(width=width,height=height,images=images)
			return concat_image
