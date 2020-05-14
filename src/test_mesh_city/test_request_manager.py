import unittest

from mesh_city.imagery_provider.request_manager import RequestManager
from mesh_city.user.quota_manager import QuotaManager
from mesh_city.user.user_info import UserInfo
from mesh_city.user.user_info_handler import UserInfoHandler


class TestRequestManager(unittest.TestCase):

	def setUp(self):
		self.user_info = UserInfo(
			"Blue", "AIzaSyD9cfAeQKFniipqRUgkcYy1sAtGXJYxNF4", 500, 25, 1452, 8, 15, 10, 55, 42
		)
		self.quota_manager = QuotaManager(self.user_info)
		self.request_manager = RequestManager(
			user_info=self.user_info, quota_manager=self.quota_manager
		)

	def test_calculate_centre_coordinates_two_coordinate_input_correct(self):
		correct_answer = "((25, 5, 5), [((-22.824266172626604, -43.242326668647785), (0, 0)), " \
                                     "((-22.824266172626604, -43.24152200594336), (1, 0)), " \
                                     "((-22.824266172626604, -43.240717343238934), (2, 0)), " \
                                     "((-22.824266172626604, -43.23991268053451), (3, 0)), " \
                                     "((-22.824266172626604, -43.239108017830084), (4, 0)), " \
                                     "((-22.823524515859624, -43.242326668647785), (0, 1)), " \
                                     "((-22.823524515859624, -43.24152200594336), (1, 1)), " \
                                     "((-22.823524515859624, -43.240717343238934), (2, 1)), " \
                                     "((-22.823524515859624, -43.23991268053451), (3, 1)), " \
                                     "((-22.823524515859624, -43.239108017830084), (4, 1)), " \
                                     "((-22.822782855052342, -43.242326668647785), (0, 2)), " \
                                     "((-22.822782855052342, -43.24152200594336), (1, 2)), " \
                                     "((-22.822782855052342, -43.240717343238934), (2, 2)), " \
                                     "((-22.822782855052342, -43.23991268053451), (3, 2)), " \
                                     "((-22.822782855052342, -43.239108017830084), (4, 2)), " \
                                     "((-22.822041190204857, -43.242326668647785), (0, 3)), " \
                                     "((-22.822041190204857, -43.24152200594336), (1, 3)), " \
                                     "((-22.822041190204857, -43.240717343238934), (2, 3)), " \
                                     "((-22.822041190204857, -43.23991268053451), (3, 3)), " \
                                     "((-22.822041190204857, -43.239108017830084), (4, 3)), " \
                                     "((-22.821299521317272, -43.242326668647785), (0, 4)), " \
                                     "((-22.821299521317272, -43.24152200594336), (1, 4)), " \
                                     "((-22.821299521317272, -43.240717343238934), (2, 4)), " \
                                     "((-22.821299521317272, -43.23991268053451), (3, 4)), " \
                                     "((-22.821299521317272, -43.239108017830084), (4, 4))]) "
		list_of_coordinates = self.request_manager.calculate_centre_coordinates_two_coordinate_input(
			(-22.824637, -43.242729), (-22.821384, -43.238813), 20
		)
		self.assertEqual(correct_answer, str(list_of_coordinates))

	def test_calculate_centre_coordinates_two_coordinate_input_invalid_input(self):
		self.assertRaises(
			Exception,
			self.request_manager.calculate_centre_coordinates_two_coordinate_input,
			(-22.821384, -43.238813), (-22.824637, -43.242729),
			20
		)
