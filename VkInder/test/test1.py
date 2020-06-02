import unittest
from unittest.mock import patch
import VkInder.vkUser.vk_api_userclass as app



access_token = 'b783b0b47736f24cf606e4c9d32d404674a55f1069ce3a073bc463c8ae0715e97c44e8c0e66e903a5f65c'



class TestVk(unittest.TestCase):
    @patch('builtins.input', return_value=access_token)
    def test_access_token(self, mock_input):
        self.assertEqual(app.User('tihon333').id, 4305103)

    def test_friends(self):
        self.assertEqual(app.User('tihon333').get_friends()[0], 11012020)

    def test_top3_photos(self):
        self.assertEqual(app.User('vindevi').get_photos()[0]['id'], 267516003)



if __name__ == '__main__':
    unittest.main()
