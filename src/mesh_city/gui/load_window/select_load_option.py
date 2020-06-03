from pathlib import Path
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

		self.load_request = Button(
			self.top, text="Previous request", command=self.load_request,
			bg="white"
		)
		self.load_request.grid(row=1)

		if "Generated" in self.building_instructions.instructions.keys():
			self.load_scenario_button = Button(
				self.top, text="Previous scenario", command=self.ask_for_scenario,
				bg="white"
			)
			self.load_scenario_button.grid(row=2)

	def load_request(self):
		LoadWindow(self.master, self.application, self.main_screen)
		self.top.destroy()

	def ask_for_scenario(self):
		self.top_label["text"] = "Which scenario do you want to load?"

		self.load_request.grid_forget()
		self.load_scenario_button.grid_forget()

		temp_counter = 1
		self.temp_dict = {}
		for key in self.building_instructions.instructions["Generated"]:
			for path in self.building_instructions.instructions["Generated"][key][1]:
				temp_path = Path(path)
				temp_name = temp_path.name
				self.temp_dict[temp_name] = temp_path
				self.scenario_button = Button(
					self.top,
					text=temp_name,
					command=lambda temp_name=temp_name: self.load_scenario(temp_name),
					bg="white"
				)
				self.scenario_button.grid(row=temp_counter)
				temp_counter += 1

	def load_scenario(self, name):
		path = self.temp_dict[name].parents[0]
		self.application.file_handler.change("active_image_path", path)
		self.main_screen.update_gif()
		self.main_screen.seen_on_screen = ["Generated"]
		self.top.destroy()

