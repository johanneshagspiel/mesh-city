"""
The module containing the eco window
"""
import math
from pathlib import Path
from tkinter import Button, Label, Scale, Toplevel

from mesh_city.detection.meta_creator import MetaCreator
from mesh_city.detection.overlay_creator import OverlayCreator

class EcoWindow:
	"""
	Window showing all the options what the user can do to make the area downloaded more eco-friendly
	"""

	def __init__(self, master, application, main_screen):
		"""
		The initialization method
		:param master: the master tkinter object
		:param application: the global application context
		:param main_screen: the main_screen of the application
		"""
		self.main_screen = main_screen
		self.master = master
		self.value = ""
		self.application = application
		self.top = Toplevel(master)

		temp_path = next(
			self.application.file_handler.folder_overview["active_request_path"].
			glob('building_instructions_request_*')
		)
		self.building_instructions = self.application.log_manager.read_log(
			temp_path, "building_instructions_request"
		)

		self.top_label = Label(self.top, text="")
		self.top_label.grid(row=0)

		if len(self.building_instructions.instructions.keys()) == 1:
			self.top_label["text"] = \
				"This area can not be made more eco-friendly. Detect something first"

		else:
			meta_creator = MetaCreator(self.application, self.building_instructions)
			meta_creator.combine_information(["Trees"])

			temp_to_read = Path.joinpath(
				self.application.file_handler.folder_overview["temp_meta_path"],
				"concat_information.csv"
			)
			self.temp_meta_info = self.application.log_manager.read_log(temp_to_read, "information")

			if self.temp_meta_info.information["Amount"] == 0:
				self.top_label["text"] = "This area can not be made more eco-friendly"

			else:
				self.top_label["text"] = "How do you want to make this area more eco-friendly?"
				self.top_label.grid(row=0)

				self.more_trees = Button(
					self.top, text="Add more trees", command=self.add_more_trees, bg="white"
				)
				self.more_trees.grid(row=1)

				self.test_scenarios = Button(
					self.top, text="Test different scenarios", command=self.test_scenarios, bg="white"
				)
				self.test_scenarios.grid(row=2)

	# pylint: disable=E0202
	def test_scenarios(self):
		"""
		A placeholder function.
		:return:
		"""
		self.top.destroy()

	def add_more_trees(self):
		"""
		Asks the user how many more trees they want in percentage
		:return: nothing (creates a gif with additional trees on it and displays that on the mainscreen)
		"""
		self.more_trees.grid_forget()
		self.test_scenarios.grid_forget()

		self.top_label["text"] = "How many trees do you want to add in percentage?"
		# pylint: disable=W0201
		self.tree_increase = Scale(self.top, from_=0, to=100, orient="horizontal")
		self.tree_increase.grid(row=1)

		confirm_button = Button(
			self.top, text="Confirm", command=self.cleanup_more_trees, bg="white"
		)
		confirm_button.grid(row=2)

	def cleanup_more_trees(self):
		"""
		creates a gif with additional trees on it and displays that on the mainscreen
		:return: nothing (a gif is created, stored, logged and shown on the mainscreen)
		"""
		increase_percentage = self.tree_increase.get() * 0.01 + 1
		trees_to_add = math.ceil(self.temp_meta_info.information["Amount"] * increase_percentage - \
                       self.temp_meta_info.information["Amount"])

		temp_overlay_creator = OverlayCreator(self.application, self.building_instructions)
		temp_overlay_creator.create_image_with_more_trees(
			trees_to_add, self.temp_meta_info, self.building_instructions
		)

		self.main_screen.update_gif()
		self.top.destroy()
