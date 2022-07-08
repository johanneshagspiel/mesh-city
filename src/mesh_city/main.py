"""
Entry module of the application.
"""
import warnings
from mesh_city.application import Application
warnings.filterwarnings('ignore')


def main() -> None:
	"""
	Entry function of the application.

	:return: Nothing.
	"""
	Application().start()


if __name__ == '__main__':
	main()
