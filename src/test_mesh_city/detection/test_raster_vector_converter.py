# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring

import pickle
from pathlib import Path
from unittest import TestCase

import numpy as np
from PIL import Image
from shapely.geometry import Polygon

from mesh_city.detection.raster_vector_converter import RasterVectorConverter


class TestRasterVectorConverter(TestCase):

	def setUp(self):
		self.rvc = RasterVectorConverter()

		self.resource_path = Path(__file__).parents[1].joinpath("resource_images")

	def test_convert_building_detections_rectangle(self):
		reference_polygon = Polygon(
			[(89.0, 162.0), (89.0, 324.0), (428.0, 324.0), (428.0, 162.0), (89.0, 162.0)]
		)
		image = np.asarray(
			Image.open(self.resource_path.joinpath("building_mask_rectangle.png")).convert("L")
		)
		polygons = self.rvc.mask_to_vector(image)
		self.assertEqual(len(polygons), 1)
		# testing coordinate lists for equality is not easy...
		np.testing.assert_array_almost_equal(
			list(zip(*polygons[0].exterior.coords.xy)),
			list(zip(*reference_polygon.exterior.coords.xy)),
			decimal=1
		)

	def test_vector_to_bounding_boxes_already_box(self):
		polygons = [Polygon([
			(89.0, 162.0),
			(89.0, 324.0),
			(428.0, 324.0),
			(428.0, 162.0),
			(89.0, 162.0),
		])]  # yapf: disable
		reference_bounding_boxes = [((89.0, 162.0), (428.0, 324.0))]

		bounding_boxes = self.rvc.vector_to_bounding_boxes(polygons=polygons)

		self.assertEqual(bounding_boxes, reference_bounding_boxes)

	def test_vector_to_bounding_boxes_cross(self):
		polygons = [Polygon([
			(206.0, 162.0),
			(206.0, 214.0),
			(89.0, 214.0),
			(89.0, 268.0),
			(214.0, 268.0),
			(214.0, 324.0),
			(300.0, 324.0),
			(300.0, 268.0),
			(428.0, 268.0),
			(428.0, 214.0),
			(300.0, 214.0),
			(300.0, 162.0),
			(206.0, 162.0),
		])]  # yapf: disable
		reference_bounding_boxes = [((89.0, 162.0), (428.0, 324.0))]

		bounding_boxes = self.rvc.vector_to_bounding_boxes(polygons=polygons)

		self.assertEqual(bounding_boxes, reference_bounding_boxes)

	def test_vector_to_bounding_boxes_multiple(self):
		polygons = [Polygon([
			(100.0, 100.0),
			(100.0, 200.0),
			(200.0, 200.0),
			(200.0, 100.0),
			(100.0, 100.0),
		]), Polygon([
			(300.0, 300.0),
			(300.0, 400.0),
			(400.0, 400.0),
			(400.0, 300.0),
			(300.0, 300.0),
		])]  # yapf: disable
		reference_bounding_boxes = [
			((100.0, 100.0), (200.0, 200.0)),
			((300.0, 300.0), (400.0, 400.0)),
		]  # yapf: disable

		bounding_boxes = self.rvc.vector_to_bounding_boxes(polygons=polygons)

		self.assertEqual(bounding_boxes, reference_bounding_boxes)
