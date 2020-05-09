""" Entry point of the application """

from mesh_city.util.google_maps.google_api_util import GoogleApiUtil


def print_start_info() -> None:
	""" Print a small splash message """
	print("Welcome to Mesh City")
	print("--------------------")


def main() -> None:
	print_start_info()

	test = GoogleApiUtil()
	test.check_key_exist()

	graaf_florisstraat_test_coordinates_box = (51.918164, 4.45569, 51.921415, 4.459962)

	test = google_maps_entity(api_util)
	test.get_area(51.918164, 4.45569, 51.921415, 4.459962, 20, 640)


if __name__ == "__main__":
	main()
