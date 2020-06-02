"""
Entry module of the application.
"""

from mesh_city.application import Application


def main() -> None:
	"""
	Entry function of the application.
	:return: Nothing.
	"""
	Application().start()


if __name__ == '__main__':
	main()
