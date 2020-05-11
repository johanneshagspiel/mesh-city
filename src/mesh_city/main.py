from mesh_city.gui.application import Application
from mesh_city.imagery_provider.request_manager import RequestManager
from mesh_city.imagery_provider.top_down_provider.ahn_provider import AhnProvider
from mesh_city.imagery_provider.user_manager import UserManager

user_manager = UserManager()
provider = AhnProvider(user_manager)
request_manager = RequestManager(user_manager)
request_manager.load_images_map(51.998967, 4.373414)
Application(request_manager)
