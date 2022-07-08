from tkinter import Entry, Label, messagebox, Toplevel, W
from mesh_city.gui.widgets.button import Button as CButton
from mesh_city.gui.widgets.container import Container
from mesh_city.gui.widgets.widget_geometry import WidgetGeometry

from mesh_city.user.image_provider_entity import ImageProviderEntity
from mesh_city.user.user_entity import UserEntity
from mesh_city.util.input_util import InputUtil
from mesh_city.util.screen_size_util import ScreenSizeUtil


class NewUserWindow:


	def __init__(self, master, application, main_screen):
		"""
		A window shown on start-up if no user exists
		:param master: the master tkinter object
		:param application: the global application context
		:param main_screen: the main screen of the application
		"""
		self.new_name_entry = None
		self.main_screen = main_screen
		self.master = master
		self.application = application
		self.top = Toplevel(master)

		self.top.config(padx=4)
		self.top.config(pady=4)

		self.top.attributes('-topmost', True)
		self.top.update()
		window_width, window_height, central_width, central_height = ScreenSizeUtil.get_curr_screen_geometry(655, 240)
		self.top.geometry("%dx%d+%d+%d" % (window_width, window_height, central_width, central_height))


		self.content = Container(WidgetGeometry(645, 230, 0, 0), self.top, background="white")
		layer_label_style = {"font": ("Eurostile LT Std", 18), "background": "white", "anchor": W}

		Label(self.content, text="Please first register as a new user", font= ("Eurostile LT Std", 18),
			  background="white").place(width=600, height=40, x=0, y=0)

		Label(self.content, text="Username", **layer_label_style,
				).place(width=260, height=40, x=0, y=40)

		self.name_text = Entry(self.content, width=20, bg="grey", font=("Eurostile LT Std", 18))
		self.name_text.place(width=360, height=40, x=280, y=40)

		Label(self.content, text="Google Maps API key", **layer_label_style,
				).place(width=260, height=40, x=0, y=80)

		self.api_key_entry = Entry(
			self.content, width=20, bg="grey", font=("Eurostile LT Std", 18)
		)
		self.api_key_entry.place(width=360, height=40, x=280, y=80)

		Label(self.content, text="Monthly API Quota", **layer_label_style,
				).place(width=260, height=40, x=0, y=120)

		self.quota_entry = Entry(self.content, width=20, bg="grey", font=("Eurostile LT Std", 18))
		self.quota_entry.place(width=360, height=40, x=280, y=120)

		CButton(
			WidgetGeometry(200, 50, 200, 170), "Create User", lambda _: self.create_user(), self.content,
		)

	def create_user(self):
		"""
		A method to check the provided information and create a new user if the information is correct.
		"""

		error_list = []

		user_name = self.name_text.get()
		if user_name == "":
			error_list.append("The Name field must be filled out.")

		google_maps_api_key = self.api_key_entry.get()
		if InputUtil.is_google_api(google_maps_api_key) is False:
			error_list.append("Google Maps API keys must start with 'AIza'.")

		quota = self.quota_entry.get()
		if quota == "" or (InputUtil.is_float(quota) is False):
			error_list.append("Quota must be a number.")
			self.quota_entry.delete(0, 'end')

		if len(error_list) > 0:

			messagebox.showinfo("Input Error", "\n".join(error_list))

		else:

			new_imagery_provider = ImageProviderEntity(file_handler=self.application.file_handler, type_map_provider="Google Maps", api_key=google_maps_api_key, quota=quota)
			new_user = UserEntity(file_handler=self.application.file_handler, name=user_name, image_providers={"Google Maps": new_imagery_provider})

			self.application.log_manager.write_log(new_user)
			self.top.destroy()
			self.main_screen.closed_popup_successfully = True
