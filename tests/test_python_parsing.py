import unittest
import ast

import python_parsing


class TestPythonParsing(unittest.TestCase):
    def test_BaseParser(self):
        class Analyzer(python_parsing.BaseParser):
            def process(self, data):
                return str(data) + "_processed"
        analyzer = Analyzer(param1="P1", param2="P2")
        self.assertEqual(analyzer.param1, "P1")
        self.assertEqual(analyzer.param2, "P2")
        self.assertEqual(analyzer.process("test"), "test_processed")

    def test_Parser(self):
        class PassThroughMixin:
            def parse(self):
                return self.syntax_tree

        class TestParser(PassThroughMixin, python_parsing.Parser):
            pass

        test_parser = TestParser()
        # OK
        self.assertEqual(
            ast.dump(test_parser.process("./python_parsing_test/build_tree_test.py")),
            "Module(body=[Assign(targets=[Name(id='a', ctx=Store())], value=Num(n=1))])"
        )
        # Bad_syntax
        self.assertIsNone(test_parser.process("./python_parsing_test/bad_syntax.py"))
        # Not a python file
        self.assertIsNone(test_parser.process("./python_parsing_test/not_python_file.txt"))

    def test_ExtractWordsFromFuncNamesMixin(self):
        class TestParser(python_parsing.ExtractWordsFromFuncNamesMixin, python_parsing.Parser):
            pass

        test_parser = TestParser()
        func_names = sorted(test_parser.process("./python_parsing_test/func_name_extraction.py"))
        self.assertListEqual(func_names, ["f3", "func1", "func2", "func3", "func4"])

    def test_ExtractVarsLocalToFunctionMixin(self):
        class TestParser(python_parsing.ExtractVarsLocalToFunctionMixin, python_parsing.Parser):
            pass

        test_parser = TestParser()
        func_names = sorted(test_parser.process("./python_parsing_test/local_vars_extraction.py"))
        self.assertListEqual(func_names, ['classvar1', 'v3', 'var11', 'var12', 'var13', 'var14', 'var2', 'var3'])


if __name__ == '__main__':
    unittest.main()
