import os
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import tensorflow as tf
from PIL import Image, ImageDraw


class CarDetector:
	"""
	the CarDetector class uses Tensorflow and a pre-trained model to detect cars from top-down imagery.
	"""

	def __init__(self) -> None:
		# Path to frozen detection graph. This is the actual model that is used for the object detection.
		frozen_graph_path = Path.joinpath(
			Path(__file__).parents[2],
			"resources",
			"neural_networks",
			"inference_graph",
			"frozen_inference_graph.pb"
		)

		# Loading a frozen Tensorflow model into memory
		self.detection_graph = tf.Graph()
		with self.detection_graph.as_default():
			od_graph_def = tf.GraphDef()
			with tf.gfile.GFile(str(frozen_graph_path), 'rb') as fid:
				serialized_graph = fid.read()
				od_graph_def.ParseFromString(serialized_graph)
				tf.import_graph_def(od_graph_def, name='')

	def detect_cars(self, image):
		with self.detection_graph.as_default():
			with tf.Session() as sess:
				# Get handles to input and output tensors
				ops = tf.get_default_graph().get_operations()
				all_tensor_names = {output.name for op in ops for output in op.outputs}
				tensor_dict = {}
				for key in [
					'num_detections',
					'detection_boxes',
					'detection_scores',
					'detection_classes',
					'detection_masks'
				]:
					tensor_name = key + ':0'
					if tensor_name in all_tensor_names:
						tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(tensor_name)

				image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

				# Run inference
				output_dict = sess.run(tensor_dict, feed_dict={image_tensor: image})

				# all outputs are float32 numpy arrays, so convert types as appropriate
				output_dict['num_detections'] = int(output_dict['num_detections'][0])
				output_dict['detection_classes'] = output_dict['detection_classes'][0].astype(
					np.int64
				)
				output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
				output_dict['detection_scores'] = output_dict['detection_scores'][0]
				if 'detection_masks' in output_dict:
					output_dict['detection_masks'] = output_dict['detection_masks'][0]
		detection_data = []
		for (bounding_box, probability) in zip(output_dict['detection_boxes'],
		                                       output_dict['detection_scores']):
			if probability > 0.5:
				detection_data.append(
					(bounding_box[1]*1024, bounding_box[0]*1024, bounding_box[3]*1024, bounding_box[2]*1024,probability,"Car"))
		df = pd.DataFrame(detection_data, columns=['xmin', 'ymin', 'xmax', 'ymax', 'score','label'])
		return df
