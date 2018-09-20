import ast
import re

from utils import *

# to gather mixins that can extract words from python names
# for example - {"func": FuncMixin, "local_var": LocalVarsMixin, ...}
NAME_EXTRACTION_MIXINS = {}


def register(registry, class_label):
    """Decorator to add class to registry dict with a key class_label"""
    def decorator_maker(cls):
        registry[class_label] = cls
        return cls
    return decorator_maker


def build_syntax_tree(program_text):
    if not program_text:
        return None
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


class Parser:
    def __init__(self, **kwargs):
        self.filename_pattern = ".*\.py$"
        for key, value in kwargs.items():
            setattr(self, key, value)

    def process(self, file_path):
        if not re.match(self.filename_pattern, file_path):
            return None
        program_text = read_file(file_path)
        self.syntax_tree = build_syntax_tree(program_text)
        return self.parse()


@register(NAME_EXTRACTION_MIXINS, "func")
class ExtractWordsFromFuncNamesMixin:
    def parse(self):
        words = []
        if not self.syntax_tree:
            return words
        func_nodes = extract_func_nodes(self.syntax_tree)
        for func_node in func_nodes:
            func_name = func_node.name.lower()
            if func_name.startswith("__") and func_name.endswith("__") and self.no_magic:
                continue
            words.extend(split_snake_case_to_words(func_name))
        return words


@register(NAME_EXTRACTION_MIXINS, "local_var")
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
            local_var_name = local_var_node.id.lower()
            if local_var_name.startswith("__") and local_var_name.endswith("__") and self.no_magic:
                continue
            words.extend(split_snake_case_to_words(local_var_name))
        return words
