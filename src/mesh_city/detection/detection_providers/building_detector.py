"""
Module containing the code interfacing with the Spacenet neural network for building detection.
"""
import cv2
import numpy as np
import torch
from torch import Tensor
from torch.autograd import Variable
from torchvision.transforms import transforms

from mesh_city.detection.detection_providers.xdxd_sn4 import XDXD_SpaceNet4_UNetVGG16


class BuildingDetector:
	"""
	The building detector class that loads a pre-trained SpaceNet and uses it to detect buildings.
	"""

	def __init__(self, nn_weights_path) -> None:
		self.model = XDXD_SpaceNet4_UNetVGG16()
		checkpoint = torch.load(nn_weights_path)
		self.model.load_state_dict(checkpoint)
		self.device = "cuda" if torch.cuda.is_available() else "cpu"
		self.model.to(self.device)
		self.image_size = 512
		self.loader = transforms.Compose([transforms.ToTensor()])
		self.per_channel_mean = np.array([95.04581181, 98.12691267, 107.52376528])
		self.per_channel_std = np.array([48.54627111, 43.82445517, 39.31087646])

	def preprocess_datum(self, datum) -> Tensor:
		"""
		Turns numpy image representation into cuda tensor
		"""
		mean_centred_datum = np.subtract(datum, self.per_channel_mean)
		scaled_datum = np.divide(
			mean_centred_datum.T, self.per_channel_std[:, np.newaxis, np.newaxis]
		).T
		datum_tensor = self.loader(scaled_datum).to(self.device, dtype=torch.float)
		datum_tensor = Variable(datum_tensor, requires_grad=False)
		datum_tensor = datum_tensor.unsqueeze(0)  # Fixes tensor shape
		return datum_tensor

	@staticmethod
	def threshold(x_value: int) -> int:
		"""
		Placeholder for more sophisticated filtering function. Is applied to each pixel to turn a
		greyscale image returned from the network into a binary classification with white pixels
		indicating where buildings were detected.

		:return: 255 if a building is detected at the pixel, 0 if not.
		"""

		if x_value >= 1:
			return 255
		return 0

	def detect(self, image):
		"""
		Method used to detect buildings on images.

		:param image: numpy representation of the image to be processed.
		:return: binary image indicating where buildings were detected.
		"""

		image_tensor = self.preprocess_datum(image)
		result = self.model(image_tensor)
		reshaped_result = result.reshape([512, 512])
		# 512x512 numpy representation of the neural network output
		unclipped_result = reshaped_result.detach().cpu().numpy()
		# clips the output to the range 0-255 to avoid image artifacts
		vec_thres = np.vectorize(BuildingDetector.threshold)
		# Creates a binary classification numpy matrix by applying vectorized threshold function
		filtered_result = vec_thres(unclipped_result)
		denoised_result = cv2.fastNlMeansDenoising(np.uint8(filtered_result), None, 11, 11, 7)

		return denoised_result
