from mesh_city.gui.application import Application
from mesh_city.imagery_provider.request_manager import RequestManager
from mesh_city.imagery_provider.top_down_provider.ahn_provider import AhnProvider
from mesh_city.imagery_provider.user_manager import UserManager


def main() -> None:
	user_manager = UserManager()
	AhnProvider(user_manager)
	request_manager = RequestManager(user_manager)
	request_manager.make_request((51.998967, 4.373414))
	Application(request_manager)


if __name__ == '__main__':
	main()
