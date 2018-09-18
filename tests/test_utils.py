import unittest
from utils import *


class TestUtils(unittest.TestCase):
    def test_is_path_remote(self):
        self.assertTrue(is_path_remote("http://example.com"))
        self.assertFalse(is_path_remote("./"))
        self.assertFalse(is_path_remote(""))
        self.assertFalse(is_path_remote(None))

    def test_dict_to_xml(self):
        xml_test = list_to_xml("xml test", [("p1", 1), ("p2", 2), ("p3", 3)])
        self.assertEqual(
            ET.tostring(xml_test, encoding="unicode"),
            "<xml test><p1>1</p1><p2>2</p2><p3>3</p3></xml test>"
        )


if __name__ == "__main__":
    unittest.main()
