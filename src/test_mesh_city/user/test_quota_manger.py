# pylint: disable=C0114,R0201,missing-class-docstring,missing-function-docstring

import unittest

from mesh_city.user.quota_manager import QuotaManager
from mesh_city.user.user_info import UserInfo


class QuotaManagerTest(unittest.TestCase):

	def setUp(self):
		self.user_info_init = UserInfo("Blue", "a12ec", 500, 25, 1452, 8, 15, 10, 55, 42)
		self.quota_manager_init = QuotaManager(self.user_info_init)

	def test_increase_usage(self):
		old_usage = self.user_info_init.usage
		manager = self.quota_manager_init
		manager.increase_usage()
		new_usage = self.user_info_init.usage
		self.assertEqual(new_usage, (old_usage + 1))

	def test_check_usage_against_quota_warning(self):
		user_info_qouta_warning = UserInfo("Blue", "a12ec", 500, 455, 1452, 8, 15, 10, 55, 42)
		manager = QuotaManager(user_info_qouta_warning)
		string_message = manager.check_usage_against_quota()
		self.assertEqual("Warning, you are getting close to your quota limit!", string_message)

	def test_check_usage_against_quota_no_warning(self):
		user_info_qouta_no_warning = UserInfo("Blue", "a12ec", 500, 4, 1452, 8, 15, 10, 55, 42)
		manager = QuotaManager(user_info_qouta_no_warning)
		string_message = manager.check_usage_against_quota()
		self.assertEqual("Within the quota", string_message)

	def test_monthly_limit_close(self):
		# This method checks the usage against the current time, how to test?
		monthly_is_close = UserInfo("Blue", "a12ec", 500, 4, 2020, 6, 15, 10, 55, 42)
		manager = QuotaManager(monthly_is_close)
		string_message = manager.check_monthly_limit(14, 7)
		self.assertEqual(
			"You are getting close to the end of the month on your quota.", string_message
		)

	def test_monthly_limit_far(self):
		# This method checks the usage against the current time, how to test?
		monthly_is_far = UserInfo("Blue", "a12ec", 500, 4, 2020, 5, 15, 10, 55, 42)
		manager = QuotaManager(monthly_is_far)
		string_message = manager.check_monthly_limit(18, 5)
		self.assertEqual("Within the monthly limit", string_message)
