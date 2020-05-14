import unittest

from mesh_city.user.quota_manager import QuotaManager
from mesh_city.user.user_info import UserInfo


class TestQuotaManager(unittest.TestCase):

	def setUp(self):
		self.user_info_init = UserInfo("Blue", "a12ec", 500, 25, 1452, 8, 15, 10, 55, 42)
		self.quota_manager_init = QuotaManager(self.user_info_init)

	def test_increase_usage(self):
		old_usage = self.user_info_init.usage
		q = self.quota_manager_init
		q.increase_usage()
		new_usage = self.user_info_init.usage
		self.assertEqual(new_usage, (old_usage + 1))

	def test_check_usage_against_quota_warning(self):
		user_info_qouta_warning = UserInfo("Blue", "a12ec", 500, 455, 1452, 8, 15, 10, 55, 42)
		q = QuotaManager(user_info_qouta_warning)
		q.check_usage_against_quota()
		#nothing to assert , should change the method to return a string GUI can also use.

	def test_check_usage_against_quota_no_warning(self):
		user_info_qouta_no_warning = UserInfo("Blue", "a12ec", 500, 4, 1452, 8, 15, 10, 55, 42)
		q = QuotaManager(user_info_qouta_no_warning)
		q.check_usage_against_quota()
		#nothing to assert

	def test_monthly_limit_close(self):
		# This method checks the usage against the current time, how to test?
		monthly_is_close = UserInfo("Blue", "a12ec", 500, 4, 2020, 6, 15, 10, 55, 42)
		q = QuotaManager(monthly_is_close)
		q.check_monthly_limit()

	def test_monthly_limit_far(self):
		# This method checks the usage against the current time, how to test?
		monthly_is_far = UserInfo("Blue", "a12ec", 500, 4, 2020, 5, 15, 10, 55, 42)
		q = QuotaManager(monthly_is_far)
		q.check_monthly_limit()


if __name__ == '__main__':
	unittest.main()
