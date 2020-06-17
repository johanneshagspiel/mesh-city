"""
source: https://stackoverflow.com/questions/43770847/play-an-animated-gif-in-python-with-tkinter
author: Novel
"""
import tkinter as tk
from itertools import count

from PIL import Image, ImageTk


# pylint: disable=W0201, W0702
class GifImage(tk.Label):
	"""a label that displays images, and plays them if they are gifs"""

	def load(self, image):
		"""
		loads an image
		:param image: the image to load (either and image or a path as a string)
		:return: nothing (the image is shown)
		"""
		if isinstance(image, str):
			image = Image.open(image)
		self.loc = 0
		self.frames = []

		try:
			for i in count(1):
				self.frames.append(ImageTk.PhotoImage(image.copy()))
				image.seek(i)
		except EOFError:
			pass

		try:
			self.delay = image.info['duration']
		except:
			self.delay = 100

		if len(self.frames) == 1:
			self.config(image=self.frames[0])
		else:
			self.next_frame()

	def unload(self):
		"""
		No image is shown any more
		:return: nothing (no image is shown any more)
		"""
		self.config(image=None)
		self.frames = None

	def next_frame(self):
		"""
		In case the image is a gif, it loads the next frame
		:return: nothing (the next frame of a gif is loaded)
		"""
		if self.frames:
			self.loc += 1
			self.loc %= len(self.frames)
			self.config(image=self.frames[self.loc])
			self.after(self.delay, self.next_frame)
