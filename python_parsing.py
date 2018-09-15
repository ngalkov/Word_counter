import ast
import abc
import re

from utils import *

# to gather mixins that can extract words from python names
# for example - {"func": FuncMixin, "local_var": LocalVarsMixin, ...}
NAME_EXTRACTION_MIXIN = {}


def register(registry, class_label):
    """Decorator to add class to registry dict with a key class_label"""
    def decorator_maker(cls):
        registry[class_label] = cls
        return cls
    return decorator_maker


def build_syntax_tree(program_text):
    try:
        syntax_tree = ast.parse(program_text)
    except SyntaxError:
        syntax_tree = None
    return syntax_tree


def extract_func_nodes(start_node):
    func_nodes = []
    if not isinstance(start_node, ast.AST):
        return func_nodes
    for node in ast.walk(start_node):
        if isinstance(node, ast.FunctionDef):
            func_nodes.append(node)
    return func_nodes


def extract_vars_from_function(func_node):
    local_var_nodes = []
    if not isinstance(func_node, ast.FunctionDef):
        return local_var_nodes
    for node in ast.iter_child_nodes(func_node):
        if isinstance(node, ast.Assign):
            for n in ast.walk(node):
                if isinstance(n, ast.Name):
                    local_var_nodes.append(n)
    return local_var_nodes


class BaseParser(abc.ABC):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @abc.abstractmethod
    def process(self, data):
        pass


class Parser(BaseParser):
    def __init__(self, **kwargs):
        self.filename_pattern = ".*\.py$"
        super().__init__(**kwargs)

    def process(self, file_path):
        if not re.match(self.filename_pattern, file_path):
            return None
        program_text = read_file(file_path)
        self.syntax_tree = build_syntax_tree(program_text)
        return self.parse()


@register(NAME_EXTRACTION_MIXIN, "func")
class ExtractWordsFromFuncNamesMixin:
    def parse(self):
        words = []
        if not self.syntax_tree:
            return words
        func_nodes = extract_func_nodes(self.syntax_tree)
        for func_node in func_nodes:
            words.extend(split_snake_case_to_words(func_node.name.lower()))
        return words


@register(NAME_EXTRACTION_MIXIN, "local_var")
class ExtractWordsFromLocalVarsMixin:
    def parse(self):
        words = []
        if not self.syntax_tree:
            return words
        func_nodes = extract_func_nodes(self.syntax_tree)
        local_var_nodes = []
        for func_node in func_nodes:
                local_var_nodes.extend(extract_vars_from_function(func_node))
        for local_var_node in local_var_nodes:
            words.extend(split_snake_case_to_words(local_var_node.id.lower()))
        return words
