from pathlib import Path

from rasterio import open, uint8
from rasterio.features import rasterize, shapes


class RasterVectorConverter:

	def convert_building_detections(self):

		with open(Path("example.png")) as file:
			image = file.read()

		polygons = [
			geometry["coordinates"] for geometry, value in shapes(source=image, mask=(image == 255))
		]

		bounding_boxes = []
		for polygon in polygons:
			for coords_group in polygon:
				top, bottom, left, right = None, None, None, None
				for image_coord in coords_group:
					if top is None:
						top = image_coord[0]
					if bottom is None:
						bottom = image_coord[0]
					if left is None:
						left = image_coord[1]
					if right is None:
						right = image_coord[1]

					top = min(image_coord[0], top)
					bottom = max(image_coord[0], bottom)
					left = min(image_coord[1], left)
					right = max(image_coord[1], right)
				bounding_boxes.append(((top, left), (bottom, right)))

		print("Number of bounding boxes:", len(bounding_boxes))

		output_image = rasterize(
			[({"coordinates": [[
			bounding_box[0],
			(bounding_box[1][0], bounding_box[0][1]),
			bounding_box[1],
			(bounding_box[0][0], bounding_box[1][1]),
			]], "type": "Polygon"}, 255) for bounding_box in bounding_boxes],
			out_shape=file.shape,
		)  # yapf: disable

		with open(
			"example_output.png",
			mode="w",
			driver="PNG",
			dtype=uint8,
			count=1,
			width=file.width,
			height=file.height,
		) as output_file:
			output_file.write(output_image, indexes=1)
