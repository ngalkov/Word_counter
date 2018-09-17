import unittest
from utils import *


class TestUtils(unittest.TestCase):
    def test_is_path_remote(self):
        self.assertTrue(is_path_remote("http://example.com"))
        self.assertFalse(is_path_remote("./"))
        self.assertFalse(is_path_remote(""))
        self.assertFalse(is_path_remote(None))


if __name__ == "__main__":
    unittest.main()
