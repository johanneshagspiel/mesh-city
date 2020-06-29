from PIL import Image

from mesh_city.detection.detection_pipeline import DetectionPipeline, DetectionType
from mesh_city.request.request_manager import RequestManager
from mesh_city.scenario.scenario_exporter import ScenarioExporter
from mesh_city.scenario.scenario_pipeline import ScenarioModificationType, ScenarioPipeline
from mesh_city.util.file_handler import FileHandler


def main() -> None:
	file_handler = FileHandler()
	request_manager = RequestManager(file_handler.folder_overview["image_path"])
	request_manager.load_data()
	pipeline = ScenarioPipeline(modification_list=[(ScenarioModificationType.PAINT_BUILDINGS_GREEN, 1572)])
	request = request_manager.get_request_by_id(1)
	scenario = pipeline.process(request)
	overlay_image = Image.open(
		file_handler.folder_overview["resource_path"].joinpath("trees-overlay.png")
	).convert("RGB")
	exporter = ScenarioExporter(
		request_manager=request_manager, overlay_image=overlay_image
	)
	exporter.export_scenario(
		scenario=scenario, export_directory=file_handler.folder_overview["resource_path"].joinpath("scenarios","1")
	)
if __name__ == '__main__':
	main()
