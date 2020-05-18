from datetime import datetime
from mesh_city.user.price_table import PriceTable


class QuotaManager:

	def __init__(self, user_info):
		self.user_info = user_info
		self.price_table = PriceTable()

	def increase_usage(self):
		old_usage = self.user_info.usage
		new_usage = old_usage + 1
		self.user_info.usage = new_usage

	def check_usage_against_quota(self):
		quota = int(self.user_info.quota)
		if (quota - self.user_info.usage) <= quota / 10:
			print("Warning, you are getting close to your quota limit!")

	def check_monthly_limit(self):
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
