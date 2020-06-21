"""
The module containing the select load option window
"""
from tkinter import Button, Label, Toplevel, W

from mesh_city.gui.load_window.load_window import LoadWindow
from mesh_city.gui.widgets.button import Button as CButton
from mesh_city.gui.widgets.container import Container
from mesh_city.gui.widgets.widget_geometry import WidgetGeometry


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

		self.top.grab_set()

		self.top.geometry("%dx%d+%d+%d" % (340, 100, 0, 0))
		layer_label_style = {"font": ("Eurostile LT Std", 18), "background": "white", "anchor": W}

		self.content = Container(WidgetGeometry(330, 100, 0, 0), self.top, background="white")

		self.top_label = Label(
			self.content, text="There is nothing to load.", **layer_label_style,
		)
		self.top_label.place(width=330, height=40, x=10, y=0)

		self.temp_dict = {}

		counter = 1
		self.to_forget_list = []

		if len(self.application.request_manager.requests) > 1:
			self.top_label["text"] = "What do you want to load?"

			load_request_button = CButton(
				WidgetGeometry(300, 50, 10, 40),
				"Load Previous Request",
				lambda _: self.load_request(),
				self.top
			)
			self.to_forget_list.append(load_request_button)
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

		for widget in self.to_forget_list:
			widget.grid_forget()

		temp_counter = 1
		for scenario_name in self.application.current_request.scenarios.keys():
			scenario_button = Button(
				self.top,
				text=scenario_name,
				command=lambda scenario_name=scenario_name: self.load_scenario(scenario_name),
				bg="white"
			)
			scenario_button.grid(row=temp_counter)
			temp_counter += 1

	def load_scenario(self, scenario_name):
		"""
		Loads the selected scenario onto the main_screen
		:param name: the name of the scenario to load
		:return: nothing (the main screen image is now the selected scenario)
		"""

		self.application.load_scenario_onscreen(name=scenario_name)
		self.top.destroy()
