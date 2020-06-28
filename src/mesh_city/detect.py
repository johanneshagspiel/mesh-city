from mesh_city.detection.detection_pipeline import DetectionPipeline, DetectionType
from mesh_city.request.request_manager import RequestManager
from mesh_city.util.file_handler import FileHandler


def main() -> None:
	file_handler = FileHandler()
	request_manager = RequestManager(file_handler.folder_overview["image_path"])
	request_manager.load_data()
	pipeline = DetectionPipeline(
		FileHandler(), request_manager, detections_to_run=[DetectionType.TREES,DetectionType.BUILDINGS,DetectionType.CARS]
	)
	request = request_manager.get_request_by_id(0)
	pipeline.process(request)

if __name__ == '__main__':
	main()
