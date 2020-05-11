""" Entry point of the application """

from mesh_city.util.google_maps.google_api_util import GoogleApiUtil
from mesh_city.util.google_maps.google_maps_entity import GoogleMapsEntity


def print_start_info() -> None:
	""" Print a small splash message """
	print("Welcome to Mesh City")
	print("--------------------")


def main() -> None:
	print_start_info()

	google_api_util = GoogleApiUtil()
	google_api_util.check_key_exist()


if __name__ == "__main__":
	main()
