import unittest
import ast

import python_parsing
from utils import *


class TestPythonParsing(unittest.TestCase):
    def test_register_decorator(self):
        self.assertEqual(
            python_parsing.NAME_EXTRACTION_MIXINS["func"],
            python_parsing.ExtractWordsFromFuncNamesMixin
        )

    def test_build_syntax_tree(self):
        self.assertEqual(
            ast.dump(python_parsing.build_syntax_tree("a = 1")),
            "Module(body=[Assign(targets=[Name(id='a', ctx=Store())], value=Num(n=1))])"
        )
        self.assertIsNone(python_parsing.build_syntax_tree("1 = 'bad syntax"))

    def test_Parser(self):
        class PassThroughMixin:
            def parse(self):
                return self.syntax_tree

        class TestParser(PassThroughMixin, python_parsing.Parser):
            pass

        test_parser = TestParser(no_magic="test")
        # test attributes defining
        self.assertEqual(test_parser.no_magic, "test")
        # test parsing OK
        self.assertEqual(
            ast.dump(test_parser.process("./python_parsing_test/build_tree_test.py")),
            "Module(body=[Assign(targets=[Name(id='a', ctx=Store())], value=Num(n=1))])"
        )
        # test bad_syntax
        self.assertIsNone(test_parser.process("./python_parsing_test/bad_syntax.py"))
        # test not a python file
        self.assertIsNone(test_parser.process("./python_parsing_test/not_python_file.txt"))

    def test_ExtractWordsFromFuncNamesMixin(self):
        class TestParser(python_parsing.ExtractWordsFromFuncNamesMixin, python_parsing.Parser):
            pass

        test_parser = TestParser()
        func_names = sorted(test_parser.process("./python_parsing_test/func_name_extraction.py"))
        self.assertListEqual(func_names, ["f3", "func1", "func2", "func3", "func4"])

    def test_ExtractWordsFromLocalVarsMixin(self):
        class TestParser(python_parsing.ExtractWordsFromLocalVarsMixin, python_parsing.Parser):
            pass

        test_parser = TestParser()
        func_names = sorted(test_parser.process("./python_parsing_test/local_vars_extraction.py"))
        self.assertListEqual(func_names, ['classvar1', 'v3', 'var11', 'var12', 'var13', 'var14', 'var2', 'var3'])


if __name__ == '__main__':
    unittest.main()
