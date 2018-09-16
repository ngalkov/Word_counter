import unittest
from words_count import *


class TestWordsCount(unittest.TestCase):
    def test_extract_words_from_python_project(self):
        # test with different set of python identifiers
        self.assertListEqual(
            sorted(extract_words_from_python_project("./projects/django", ["func", "local_var"])),
            ['do', 'get', 'make', 'make', 'query', 'query', 'table', 'table', 'table']
        )
        self.assertListEqual(
            sorted(extract_words_from_python_project("./projects/django", ["func"])),
            ['do', 'get', 'make', 'make', 'query', 'table', 'table']
        )
        self.assertListEqual(extract_words_from_python_project("./projects/django", []), [])

    def test_count_part_of_speech_in_python_projects(self):
        # test with different set of part of speech
        words_statistics = count_part_of_speech_in_python_projects(
            ["./projects/django", "./projects/flask", "./projects/pyramid"],
            ["func", "local_var"],
            ["verb", "noun"]
        )
        self.assertDictEqual(words_statistics,
                             {'make': 4, 'query': 4, 'table': 4, 'get': 2, 'do': 2, 'address': 2, 'find': 1})
        words_statistics = count_part_of_speech_in_python_projects(
            ["./projects/django"],
            ["func", "local_var"],
            ["verb"]
        )
        self.assertDictEqual(words_statistics, {'make': 2, 'get': 1, 'do': 1})
        # test empty arguments
        self.assertDictEqual(count_part_of_speech_in_python_projects([], ["func"], ["verb"]), {})
        self.assertDictEqual(count_part_of_speech_in_python_projects(["./projects/django"], [], ["verb"]), {})
        self.assertDictEqual(count_part_of_speech_in_python_projects(["./projects/django"], ["func"], []), {})


if __name__ == "__main__":
    unittest.main()
