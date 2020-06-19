"""
See :class:`.ScenarioExporter`
"""
from pathlib import Path

from PIL import Image

from mesh_city.gui.scenario_renderer import ScenarioRenderer
from mesh_city.request.layers.google_layer import GoogleLayer
from mesh_city.request.request_exporter import RequestExporter
from mesh_city.request.request_manager import RequestManager
from mesh_city.scenario.scenario import Scenario
from mesh_city.util.geo_location_util import GeoLocationUtil


class ScenarioExporter:
	"""
	An exporter for scenarios
	"""

	def __init__(self, request_manager: RequestManager, overlay_image: Image):
		self.request_manager = request_manager
		self.overlay_image = overlay_image

	def export_scenario(self, scenario: Scenario, export_directory: Path) -> None:
		"""
		Exports a single layer from a request using methods specific to the type of the layer.

		:param request: The request that contains the layer to be exported
		:param index: The index of the layer that is to be exported.
		:param export_directory:  The root of the directory layers should be exported to.
		:return: None
		"""
		request = scenario.request
		image_layer = request.get_layer_of_type(GoogleLayer)
		scenario_renderer = ScenarioRenderer(overlay_image=self.overlay_image)
		for tile in image_layer.tiles:
			result_image = Image.open(tile.path).convert("RGB")
			origin_path = tile.path
			rel_path = origin_path.relative_to(self.request_manager.get_image_root())
			export_directory.joinpath(rel_path.parent).mkdir(parents=True, exist_ok=True)
			x_offset = (tile.x_grid_coord - request.x_grid_coord) * 1024
			y_offset = (tile.y_grid_coord - request.y_grid_coord) * 1024
			if scenario.buildings is not None:
				buildings = scenario.buildings.copy(deep=True)
				buildings.geometry = buildings.geometry.translate(xoff=-x_offset,yoff=-y_offset,zoff=0)
				result_image = scenario_renderer.render_shrubbery(base_image=result_image,
				                                                  buildings=buildings,
				                                                  overlay_image=self.overlay_image,
				                                                  scaling=1)
			result_image.save(export_directory.joinpath(rel_path))
			nw_latitude, nw_longitude = GeoLocationUtil.tile_value_to_degree(
				x_cor_tile=tile.x_grid_coord + 0.5,
				y_cor_tile=tile.y_grid_coord + 0.5,
				zoom=request.zoom,
				get_centre=False
			)
			filename_no_extension = origin_path.stem
			world_file_name = filename_no_extension + ".pgw"
			RequestExporter.create_world_file(
				path=export_directory.joinpath(rel_path.parent, world_file_name),
				latitude=nw_latitude,
				longitude=nw_longitude,
				zoom=request.zoom,
				width=1024,
				height=1024
			)
