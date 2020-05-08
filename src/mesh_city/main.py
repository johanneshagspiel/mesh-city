""" Entry point of the application """
from mesh_city.util.google_maps.google_api_util import google_api_util
from mesh_city.util.google_maps.google_maps_entity import google_maps_entity
from mesh_city.gui.self_made_map import self_made_map

#test = google_api_util()
#test2 = google_maps_entity(test)

#test2.load_images_map(51.923699, 5.492631)
#test2.load_images_map(51.998875, 4.373495)

test = self_made_map()
test


def print_start_info() -> None:
	""" Print a small splash message """
	print("Welcome to Mesh City")
	print("--------------------")


if __name__ == "__main__":
	print_start_info()
