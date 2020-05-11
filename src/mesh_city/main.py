from mesh_city.gui.self_made_map import self_made_map
from mesh_city.util.google_maps.google_api_util import GoogleApiUtil
from mesh_city.util.google_maps.google_maps_entity import GoogleMapsEntity
from mesh_city.util.mapbox.mapbox_entity import mapbox_entity
from mesh_city.util.request_manager import RequestManager

test = GoogleApiUtil()
test2 = mapbox_entity(test)
test3 = RequestManager(test)
#test3.concat_images()
test3.load_images_map(50,50)
test4 = self_made_map(test3)
test4
