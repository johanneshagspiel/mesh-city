import tkinter as tk

class ScreenSizeUtil:
    """
    A helper class to determine the location to spawn the window in the center of the display
    """

    @staticmethod
    def get_curr_screen_geometry(window_width, window_height):
        """
        The method to determine the location to spawn a window in the center of the display
        """

        root = tk.Tk()
        root.update_idletasks()
        root.attributes('-fullscreen', True)
        root.state('iconic')
        geometry = root.winfo_geometry()
        root.destroy()

        width, height = geometry.split("+")[0].split("x")

        central_width, central_height = (int(width) - window_width) / 2, (int(height) - window_height) / 2

        return window_width, window_height, central_width, central_height
