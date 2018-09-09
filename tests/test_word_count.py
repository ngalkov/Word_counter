import unittest

from natural_language_processing import *


class TestNaturalLanguageProcessing(unittest.TestCase):
    def test_BaseAnalyzer(self):
        class Analyzer(BaseAnalyzer):
            def process(self, data):
                return str(data) + "_processed"
        analyzer = Analyzer(param1="P1", param2="P2")
        self.assertEqual(analyzer.param1, "P1")
        self.assertEqual(analyzer.param2, "P2")
        self.assertEqual(analyzer.process("test"), "test_processed")

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
        nv_filter = PartOfSpeechFilter(("noun", "verb"))
        words = ("", "get", "makes" "word", "python", "123")
        filtered = ["get", "makes" "word", "python"]
        self.assertEqual(nv_filter.process(words), filtered)


if __name__ == '__main__':
    unittest.main()
