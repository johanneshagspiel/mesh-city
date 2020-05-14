from datetime import datetime

from mesh_city.user.price_table import PriceTable


class QuotaManager:
	"""
	This class is used to manage the quota that is initially inputted by the user.
	It should throw warning to the user if the qouta is being reached or is over it.
	"""
	def __init__(self, user_info):
		self.user_info = user_info
		self.price_table = PriceTable()

	def increase_usage(self):
		"""
		This method increases the usage variable.
		"""
		old_usage = self.user_info.usage
		new_usage = old_usage + 1
		self.user_info.usage = new_usage

	def check_usage_against_quota(self):
		"""
		This method checks that the usage doesn't go above the qouta and if it does it prints
		a warning.
		:return:
		"""
		quota = int(self.user_info.quota)
		if (quota - self.user_info.usage) <= quota / 10:
			print("Warning, you are getting close to your quota limit!")

	def check_monthly_limit(self):
		"""
		This method checks the initial date when the quota was inputted and checks whether or not
		the monthly quota renewal is close.
		:return:
		"""
		init_date = datetime(self.user_info.year, self.user_info.month, self.user_info.day, )
		diff_months = datetime.now().month - init_date.month
		diff_days = datetime.now().day - init_date.day

		if diff_months == 0:
			# We good? or are there edge cases in the monthly billing?
			print("within the monthly limit")
		if diff_months == 1 & diff_days >= -3:
			print("You are getting close to the end of the month on your quota.")
		else:
			print("You should renew your quota.")
