from mesh_city.gui.self_made_map import self_made_map
from mesh_city.imagery_provider.user_entity import UserEntity
from mesh_city.imagery_provider.map_provider.mapbox_entity import MapboxEntity
from mesh_city.imagery_provider.map_provider.google_maps_entity import GoogleMapsEntity
from mesh_city.imagery_provider.map_provider.ahn_entity import AhnEntity
from mesh_city.imagery_provider.request_manager import RequestManager

test = UserEntity()
test2 = AhnEntity(test)
test3 = RequestManager(test)
#test3.concat_images()
test3.load_images_map(51.998967, 4.373414)
test4 = self_made_map(test3)
test4
