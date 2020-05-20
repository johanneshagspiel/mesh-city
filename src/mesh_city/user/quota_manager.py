"""
See :class:`.QuotaManager`
"""

from datetime import datetime


class QuotaManager:
	"""
	This class is used to manage the quota that is initially inputted by the user.
	It should throw warning to the user if the qouta is being reached or is over it.
	"""

	def __init__(self, user_info):
		self.user_info = user_info

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
			return "Warning, you are getting close to your quota limit!"
		return "Within the quota"

	def check_monthly_limit(self, current_day, current_month):
		"""
		This method checks the initial date when the quota was inputted and checks whether or not
		the monthly quota renewal is close.
		:param: Gets the day and the month to compare to.
		:return: String message giving the appropriate message
		"""
		init_date = datetime(self.user_info.year, self.user_info.month, self.user_info.day, )
		diff_months = current_month - init_date.month
		diff_days = current_day - init_date.day

		if diff_months == 1 & diff_days >= -3:
			return "You are getting close to the end of the month on your quota."
		return "Within the monthly limit"

	def get_current_day(self):
		"""
		Gets the current day.(used in conjunction with the check_monthly_limit method.)
		:return: The current day.
		"""
		return datetime.now().day

	def get_current_month(self):
		"""
		Gets the current month.(used in conjunction with the check_monthly_limit method.)
		:return: The current month.
		"""
		return datetime.now().month
