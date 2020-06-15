

class RequestObserver:

	def __init__(self):
		self.total_images = 0
		self.current_image = 0
		self.missing_images = 0
		self.current_time_download = 0
		self.duration_so_far = 0
		self.estimated_time_to_finish = 0

	def update(self, request_maker):
		self.total_images = request_maker.state["total_images"]
		self.current_image = request_maker.state["current_image"]
		self.current_time_download = request_maker.state["current_time_download"]
		self.update_estimated_time_to_finish()

	def update_estimated_time_to_finish(self):
		self.missing_images = self.total_images - self.current_image
		self.duration_so_far += self.current_time_download
		self.estimated_time_to_finish = self.missing_images * (self.duration_so_far / self.current_image)
