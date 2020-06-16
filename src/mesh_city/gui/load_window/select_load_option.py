"""
The module containing the select load option window
"""
from pathlib import Path
from tkinter import Button, Label, Toplevel

from mesh_city.gui.load_window.load_window import LoadWindow


class SelectLoadOption:
	"""
	The class where the user can select what they want to load: previous request and if they exist
	previously created scenarios from the eco window
	"""

	# pylint: disable=E0202, W0702
	def __init__(self, master, application, main_screen):
		"""
		Asks the user what they want to load: a previous request or if they exist a previously created scenario
		:param master: the master tkinter application
		:param application: the global application context
		:param main_screen: the main_screen of the application
		"""
		self.master = master
		self.value = ""
		self.application = application
		self.main_screen = main_screen
		self.top = Toplevel(master)

		self.top.config(padx=4)
		self.top.config(pady=4)

		self.temp_dict = {}

		self.top_label = Label(self.top, text="What do you want to load?")
		self.top_label.grid(row=0)

		counter = 1

		if len(self.application.request_manager.requests) > 1:
			self.load_request = Button(
				self.top, text="Previous request", command=self.load_request, bg="white"
			)
			self.load_request.grid(row=counter)
			counter += 1

		if len(self.application.current_request.scenarios) > 0:
			self.load_scenario_button = Button(
				self.top, text="Previous scenario", command=self.ask_for_scenario, bg="white"
			)
			self.load_scenario_button.grid(row=counter)
			counter += 1

	def load_request(self):
		"""
		Opens the load window where the user can select which request to load
		:return: nothing (the load window is opened)
		"""
		LoadWindow(self.master, self.application, self.main_screen)
		self.top.destroy()

	def ask_for_scenario(self):
		"""
		The window is changed to now ask the user which of the previously created scenarios they want to load
		:return:
		"""
		self.top_label["text"] = "Which scenario do you want to load?"

		self.load_request.grid_forget()
		self.load_scenario_button.grid_forget()

		temp_counter = 1
		for scenario in self.application.current_request.scenarios:
			temp_name = scenario.scenario_index
			temp_index = scenario.scenario_index
			scenario_button = Button(
				self.top,
				text=temp_name,
				command=lambda temp_index=temp_index: self.load_scenario(temp_index),
				bg="white"
			)
			scenario_button.grid(row=temp_counter)
			temp_counter += 1

	def load_scenario(self, temp_index):
		"""
		Loads the selected scenario onto the main_screen
		:param name: the name of the scenario to load
		:return: nothing (the main screen image is now the selected scenario)
		"""

		self.application.load_scenario_onscreen(request=self.application.current_request,
		                                        scenario_index=temp_index)
		self.top.destroy()
