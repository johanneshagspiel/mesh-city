"""
See :class:`.RasterVectorConverter`
"""

from tkinter import Image
from typing import Sequence

from rasterio.features import shapes
from shapely.geometry import Polygon
from shapely.geometry import shape


class RasterVectorConverter:
	"""
	Provides tools to turn raster output of neural networks into vector representations thereof.
	"""

	@staticmethod
	def mask_to_vector(image: Image) -> Sequence[Polygon]:
		"""
		Turns a mask image with white shapes into a simplified polygon representation.

		:param image: Pillow image object
		:return: GeoJSON-like dicts representing detected polygons.
		"""
		shapes_from_mask = [shape(geometry) for geometry, value in shapes(source=image, mask=(image == 255))]
		simplified_shapes = [shape_from_mask.simplify(10, preserve_topology=False) for shape_from_mask in shapes_from_mask]
		return simplified_shapes

	@staticmethod
	def vector_to_bounding_boxes(polygons: Sequence[Polygon]) -> [((int, int), (int, int))]:
		"""
		Determines the bounding boxes of one or more polygons.

		:param polygons: A nested list of polygons.
		:return: A list of bounding boxes. The first component is the top-left, the second the
		         bottom-right.
		"""
		bounding_boxes = []
		for polygon in polygons:
			top, left, bottom, right = polygon.bounds
			bounding_boxes.append(((top, left), (bottom, right)))
		return bounding_boxes
