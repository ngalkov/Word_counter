import unittest

from natural_language_processing import *


class TestNaturalLanguageProcessing(unittest.TestCase):
    def test_tag_part_of_speech(self):
        cases = (
            (None, None),
            ("", None),
            ("get", "verb"), ("GET", "verb"), ("gets", "verb"), ("got", "verb"),
            ("python", "noun"),
            ("123", None),
        )
        for word, tag in cases:
            self.assertEqual(tag_part_of_speech(word), tag)

    def test_PartOfSpeechFilter(self):
        noun_verb_filter = PartOfSpeechFilter(("noun", "verb"))
        noun_filter = PartOfSpeechFilter(["noun"])
        words = ("", "get", "makes", "word", "python", "123")
        self.assertEqual(noun_verb_filter.process(words), ["get", "makes", "word", "python"])
        self.assertEqual(noun_filter.process(words), ["word", "python"])

if __name__ == '__main__':
    unittest.main()
