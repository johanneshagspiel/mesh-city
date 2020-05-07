""" Entry point of the application """
from .util.google_maps import google_api_util, google_maps_entity

test = google_api_util.google_api_util()
test2 = google_maps_entity.google_maps_entity(test)

test2.get_and_store_location(47.503029,9.754461)

print('Running main...')
