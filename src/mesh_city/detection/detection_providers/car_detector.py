# pylint: disable=E1129
"""
See :class:`.CarDetector`
"""

from pathlib import Path

import numpy as np
import pandas as pd
import tensorflow as tf


class CarDetector:
	"""
	The CarDetector class uses Tensorflow and a pre-trained model to detect cars from top-down imagery.
	"""

	def __init__(self) -> None:
		# Path to frozen detection graph. This is the actual model that is used for the object detection.
		frozen_graph_path = Path.joinpath(
			Path(__file__).parents[2], "resources", "neural_networks", "car_inference_graph.pb"
		)

		# Loading a frozen Tensorflow model into memory
		self.detection_graph = tf.Graph()
		with self.detection_graph.as_default():
			od_graph_def = tf.GraphDef()
			with tf.gfile.GFile(str(frozen_graph_path), 'rb') as fid:
				serialized_graph = fid.read()
				od_graph_def.ParseFromString(serialized_graph)
				tf.import_graph_def(od_graph_def, name='')
			self.session = tf.Session()
			ops = tf.get_default_graph().get_operations()
			all_tensor_names = {output.name for op in ops for output in op.outputs}
			self.tensor_dict = {}
			for key in [
				'num_detections',
				'detection_boxes',
				'detection_scores',
				'detection_classes',
				'detection_masks'
			]:
				tensor_name = key + ':0'
				if tensor_name in all_tensor_names:
					self.tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(tensor_name)

	def close(self):
		"""
		Closes the tensorflow sesssion after all cars have been detected. The detector becomes
		unusable by doing this.
		:return:
		"""
		self.session.close()

	def detect_cars(self, image):
		"""
		Detects cars from a numpy representation of an image.
		:param image: The image
		:return: A dataframe representation of the car detections.
		"""
		with self.detection_graph.as_default():
			image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

			# Run inference
			output_dict = self.session.run(self.tensor_dict, feed_dict={image_tensor: image})

			# all outputs are float32 numpy arrays, so convert types as appropriate
			output_dict['num_detections'] = int(output_dict['num_detections'][0])
			output_dict['detection_classes'] = output_dict['detection_classes'][0].astype(np.int64)
			output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
			output_dict['detection_scores'] = output_dict['detection_scores'][0]
			if 'detection_masks' in output_dict:
				output_dict['detection_masks'] = output_dict['detection_masks'][0]
		detection_data = []
		for (bounding_box,
			probability) in zip(output_dict['detection_boxes'], output_dict['detection_scores']):
			if probability > 0.99:
				detection_data.append(
					(
					bounding_box[1] * 1024,
					bounding_box[0] * 1024,
					bounding_box[3] * 1024,
					bounding_box[2] * 1024,
					probability,
					"Car"
					)
				)
		dataframe = pd.DataFrame(
			detection_data, columns=['xmin', 'ymin', 'xmax', 'ymax', 'score', 'label']
		)
		return dataframe
