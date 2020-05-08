""" Entry point of the application """

from mesh_city.util.google_maps.google_api_util import google_api_util


def print_start_info() -> None:
	""" Print a small splash message """
	print("Welcome to Mesh City")
	print("--------------------")


def main() -> None:
	print_start_info()

	test = google_api_util()
	test.check_key_exist()


if __name__ == "__main__":
	main()
