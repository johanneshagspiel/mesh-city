"""
Module containing the deep_forest tree detection algorithm
"""

import numpy as np
import torch
from PIL import Image
from torch.autograd import Variable
from torchvision import transforms

from mesh_city.detection.detection_providers.xdxd_sn4 import XDXD_SpaceNet4_UNetVGG16
from mesh_city.util.image_util import ImageUtil


class BuildingDetector:
	"""
	The building detector class that loads a pre-trained SpaceNet and uses it to detect buildings.
	"""

	def __init__(self, file_handler):
		self.file_handler = file_handler
		self.model = XDXD_SpaceNet4_UNetVGG16()
		checkpoint = torch.load(
			self.file_handler.folder_overview["resource_path"].
			joinpath("neural_networks/xdxd_spacenet4_solaris_weights.pth")
		)
		self.model.load_state_dict(checkpoint)
		self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
		if self.device == 'cuda':
			self.model.cuda()
		self.image_size = 512
		self.loader = transforms.Compose([transforms.Scale(self.image_size), transforms.ToTensor()])

	def image_loader(self, image_name):
		"""load image, returns cuda tensor"""
		large_image = Image.open(image_name)
		# Scales the image to the range [-6,6], which is currently a heuristic.
		image = (
			self.loader(large_image.resize((self.image_size, self.image_size))
					).float().to(self.device) * 2 - 1
		) * 6
		large_image.close()
		image = Variable(image, requires_grad=False)
		image = image.unsqueeze(0)  # this is for VGG, may not be needed for ResNet
		return image  # assumes that you're using GPU

	@staticmethod
	def threshold(x_value):
		"""
		Placeholder for more sophisticated filtering function. Is applied to each pixel to turn a
		greyscale image returned from the network into a binary classification with white pixels
		indicating where buildings were detected.
		:return: 255 if a building is detected at the pixel, 0 if not.
		"""
		if x_value > 128:
			return 255
		return 0

	def detect(self, image_path):
		"""
		Method used to detect buildings on images
		:param image_path: path where the image is stored from which to detect buildings
		:return: binary image indicating where buildings were detected.
		"""
		image = self.image_loader(image_path)
		result = self.model(image)
		reshaped_result = result.reshape([512, 512])
		# a 512x512 numpy representation of the neural network output
		unclipped_result = reshaped_result.detach().cpu().numpy()
		# clips the output to the range 0-255 to avoid image artifacts
		clipped_result = np.clip(
			255 * (unclipped_result - np.min(unclipped_result)) / np.ptp(unclipped_result).astype(int),
			0,
			255
		)
		vec_thres = np.vectorize(BuildingDetector.threshold)
		# creates a binary classification numpy matrix by applying vectorized threshold function
		filtered_result = vec_thres(clipped_result)
		# returns the corresponding PIL image
		return ImageUtil.greyscale_matrix_to_image(filtered_result)
