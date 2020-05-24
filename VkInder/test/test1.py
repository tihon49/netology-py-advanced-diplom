import unittest
from VkInder.main import *
from VkInder.vkUser.vk_api_userclass import User


class TestVk(unittest.TestCase):
    def test_User_id(self):
        self.assertEqual(User('tihon333').id, 4305103)

    def test_friends_get(self):
        self.assertEqual(check_users_params(User('tihon333'))['first_name'], 'Александр')



if __name__ == '__main__':
    unittest.main()