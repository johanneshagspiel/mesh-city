"""
Module containing the code interfacing with the Spacenet neural network for building detection.
"""

import numpy as np
import torch
from torch.autograd import Variable
from torchvision.transforms import transforms

from mesh_city.detection.detection_providers.xdxd_sn4 import XDXD_SpaceNet4_UNetVGG16


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
		self.model.to(self.device)
		self.image_size = 512
		self.loader = transforms.Compose([transforms.ToTensor()])

	def preprocess_datum(self, datum):
		"""Turns numpy image representation into cuda tensor"""
		# Scales the image to the range [-6,6], which is currently a heuristic.
		datum_tensor = (self.loader(datum).to(self.device) * 2 - 1) * 6
		datum_tensor = Variable(datum_tensor, requires_grad=False)
		datum_tensor = datum_tensor.unsqueeze(0)  # Fixes tensor shape
		return datum_tensor

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

	def detect(self, image):
		"""
		Method used to detect buildings on images
		:param image: numpy representation of the image to be processed.
		:return: binary image indicating where buildings were detected.
		"""
		image_tensor = self.preprocess_datum(image)
		result = self.model(image_tensor)
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
		return filtered_result