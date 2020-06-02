from tkinter import Button, Label, Toplevel
from mesh_city.gui.load_window.load_window import LoadWindow

class SelectLoadOption:

	def __init__(self, master, application, main_screen):
		"""
		First asks the user which request to export
		:param master: the master tkinter application
		:param application: the global application context
		"""
		self.master = master
		self.value = ""
		self.application = application
		self.main_screen = main_screen
		self.top = Toplevel(master)

		temp_path = next(
			self.application.file_handler.folder_overview["active_request_path"].
			glob('building_instructions_request_*')
		)
		self.building_instructions = self.application.log_manager.read_log(
			temp_path, "building_instructions_request"
		)

		self.top_label = Label(self.top, text="What do you want to load?")
		self.top_label.grid(row=0)

		self.load_scenario = Button(
			self.top, text="Previous request", command=self.load_scenario,
			bg="white"
		)
		self.load_scenario.grid(row=1)


		if "Generated" in self.building_instructions.instructions.keys():
			self.load_scenario = Button(
				self.top, text="Previous scenario", command=self.load_scenario,
				bg="white"
			)
			self.load_scenario.grid(row=2)

	def load_scenario(self):
		self.top_label["text"] = "Which scenario do you want to load?"

		for key in self.building_instructions["Generated"]:
			for value in self.building_instructions["Generated"][key].values():
				temp_name = value.name
				self.temp_button = Button(
					self.top, text="Load previous scenario", command=self.load_scenario,
					bg="white"
				)
				self.load_scenario.grid(row=3)

	def load_request(self):
		LoadWindow(self.master, self.application, self.main_screen)
		self.top.destroy()
