"""
Entry module of the application.

51.923570
4.492583

51.925856
4.496654

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
