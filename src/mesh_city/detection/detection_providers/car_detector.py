import os
import sys
import tarfile
import zipfile
from collections import defaultdict
from distutils.version import StrictVersion
from io import StringIO
from pathlib import Path

import cv2
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import six.moves.urllib as urllib
import tensorflow as tf
import tf_slim as slim
from PIL import Image

from mesh_city.util.object_detection.utils import (
	label_map_util, ops as utils_ops, visualization_utils as vis_util,
)


class CarDetector:
	"""
	the CarDetector class uses Tensorflow and pre-trained model to detect cars from top-down imagery.
	"""

	MODEL_NAME = 'inference_graph'
	# Path to frozen detection graph. This is the actual model that is used for the object detection.
	pure_path_to_frozen_graph = Path.joinpath(
		Path(__file__).parents[2],
		"resources",
		"neural_networks",
		str(MODEL_NAME),
		"frozen_inference_graph.pb"
	)
	PATH_TO_FROZEN_GRAPH = str(pure_path_to_frozen_graph)
	# List of the strings that is used to add correct label for each box.
	pure_path_to_labels = Path.joinpath(
		Path(__file__).parents[2], "resources", "neural_networks", "car_model", "labelmap.pbtxt"
	)
	PATH_TO_LABELS = str(pure_path_to_labels)

	# Loading a frozen Tensorflow model into memory
	detection_graph = tf.Graph()
	with detection_graph.as_default():
		od_graph_def = tf.GraphDef()
		with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
			serialized_graph = fid.read()
			od_graph_def.ParseFromString(serialized_graph)
			tf.import_graph_def(od_graph_def, name='')

	# Loading label map
	category_index = label_map_util.create_category_index_from_labelmap(
		PATH_TO_LABELS, use_display_name=True
	)
	# temp code:
	# For the sake of simplicity we will use only 2 images:
	# image1.jpg
	# image2.jpg
	# If you want to test the code with your images, just add path to the images to the TEST_IMAGE_PATHS.
	TEST_IMAGE_PATHS = [
		os.path.join(
		str(Path.joinpath(Path(__file__).parents[0], "test_images")), 'image{}.png'.format(i)
		) for i in range(1, 3)
	]

	# Size, in inches, of the output images.
	IMAGE_SIZE = (12, 8)

	def run_inference_for_single_image(image, graph):
		with graph.as_default():
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
				if 'detection_masks' in tensor_dict:
					# The following processing is only for single image
					detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
					detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
					# Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
					real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
					detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
					detection_masks = tf.slice(
						detection_masks, [0, 0, 0], [real_num_detection, -1, -1]
					)
					detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
						detection_masks, detection_boxes, image.shape[1], image.shape[2]
					)
					detection_masks_reframed = tf.cast(
						tf.greater(detection_masks_reframed, 0.5), tf.uint8
					)
					# Follow the convention by adding back the batch dimension
					tensor_dict['detection_masks'] = tf.expand_dims(detection_masks_reframed, 0)
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
		return output_dict

	for image_path in TEST_IMAGE_PATHS:
		image = Image.open(image_path)
		# the array based representation of the image will be used later in order to prepare the
		# result image with boxes and labels on it. changed it to work with OpenCV
		image_np = cv2.imread(image_path, 1)
		# Expand dimensions since the model expects images to have shape: [1, None, None, 3]
		image_np_expanded = np.expand_dims(image_np, axis=0)
		# Actual detection.
		output_dict = run_inference_for_single_image(image_np_expanded, detection_graph)
		# Visualization of the results of a detection.
		vis_util.visualize_boxes_and_labels_on_image_array(
			image_np,
			output_dict['detection_boxes'],
			output_dict['detection_classes'],
			output_dict['detection_scores'],
			category_index,
			instance_masks=output_dict.get('detection_masks'),
			use_normalized_coordinates=True,
			line_thickness=8
		)
		plt.figure(figsize=IMAGE_SIZE)
		plt.imshow(image_np)
		matplotlib.use('tkagg')
		plt.show()
