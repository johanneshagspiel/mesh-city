# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring

import pickle
from pathlib import Path
from unittest import TestCase

from mesh_city.detection.raster_vector_converter import RasterVectorConverter


class TestRasterVectorConverter(TestCase):

	def setUp(self):
		self.rvc = RasterVectorConverter()
		self.resource_path = Path("src/test_mesh_city/resource_images")

	def test_convert_building_detections_rectangle(self):
		reference_polygons = [[[
			(89.0, 162.0),
			(89.0, 324.0),
			(428.0, 324.0),
			(428.0, 162.0),
			(89.0, 162.0),
		]]]  # yapf: disable

		polygons = self.rvc.mask_to_vector(
			self.resource_path.joinpath("building_mask_rectangle.png")
		)

		self.assertEqual(polygons, reference_polygons)

	def test_convert_building_detections_complex(self):
		with self.resource_path.joinpath("building_polygons").open("rb") as file:
			reference_polygons = pickle.load(file=file)

		polygons = self.rvc.mask_to_vector(
			detection_mask=self.resource_path.joinpath("building_mask_complex.png")
		)

		self.assertEqual(polygons, reference_polygons)

	def test_vector_to_bounding_boxes_already_box(self):
		polygons = [[[
			(89.0, 162.0),
			(89.0, 324.0),
			(428.0, 324.0),
			(428.0, 162.0),
			(89.0, 162.0),
		]]]  # yapf: disable
		reference_bounding_boxes = [((89.0, 162.0), (428.0, 324.0))]

		bounding_boxes = self.rvc.vector_to_bounding_boxes(polygons=polygons)

		self.assertEqual(bounding_boxes, reference_bounding_boxes)

	def test_vector_to_bounding_boxes_cross(self):
		polygons = [[[
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
		]]]  # yapf: disable
		reference_bounding_boxes = [((89.0, 162.0), (428.0, 324.0))]

		bounding_boxes = self.rvc.vector_to_bounding_boxes(polygons=polygons)

		self.assertEqual(bounding_boxes, reference_bounding_boxes)

	def test_vector_to_bounding_boxes_multiple(self):
		polygons = [[[
			(100.0, 100.0),
			(100.0, 200.0),
			(200.0, 200.0),
			(200.0, 100.0),
			(100.0, 100.0),
		]], [[
			(300.0, 300.0),
			(300.0, 400.0),
			(400.0, 400.0),
			(400.0, 300.0),
			(300.0, 300.0),
		]]]  # yapf: disable
		reference_bounding_boxes = [
			((100.0, 100.0), (200.0, 200.0)),
			((300.0, 300.0), (400.0, 400.0)),
		]  # yapf: disable

		bounding_boxes = self.rvc.vector_to_bounding_boxes(polygons=polygons)

		self.assertEqual(bounding_boxes, reference_bounding_boxes)
