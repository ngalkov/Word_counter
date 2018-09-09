import ast
import abc
import re


def read_file(file_path):
    """Return file content or None in case of error"""
    try:
        with open(file_path) as fp:
            return fp.read()
    except OSError:
        return None

class BaseParser(abc.ABC):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @abc.abstractmethod
    def process(self, data):
        pass


class PythonParser(BaseParser):
    def __init__(self, **kwargs):
        self.filename_pattern = ".*\.py$"
        super().__init__(**kwargs)

    def process(self, file_path):
        if not re.match(self.filename_pattern, file_path):
            return None
        program_text = read_file(file_path)
        try:
            syntax_tree = ast.parse(program_text)
        except SyntaxError:
            syntax_tree = None
        return self.parse(syntax_tree)


class ExtractWordsFromFuncNamesMixin():
    def parse(self, syntax_tree):
        words = []
        if not syntax_tree:
            return words
        for node in ast.walk(syntax_tree):
            if isinstance(node, ast.FunctionDef):
                words.extend(split_snake_case_to_words(node.name.lower()))
        return words


def split_snake_case_to_words(name):
    return [word for word in name.split('_') if word]
