from tkinter import Tk
from mesh_city.gui.self_made_map import SelfMadeMap

def main() -> None:
	master = Tk()
	master.title("Google maps extractor")
	master.geometry("")
	app = SelfMadeMap(master)


if __name__ == '__main__':
	main()
