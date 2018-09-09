"""Collect verb usage statistics through projects"""


import os
import argparse
from collections import Counter

from code_processing import PythonParser, ExtractWordsFromFuncNamesMixin
from natural_language_processing import Analyzer, FilterPartOfSpeechMixin


def parse_cmd_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--dir",
        help="path to directory with projects",
        default="./",
    )
    parser.add_argument(
        "-p", "--projects",
        nargs='+',
        help="projects list to check",
        default=[]
    )
    parser.add_argument(
        "-l", "--projects_list",
        help="file with projects list to check"
    )
    parser.add_argument(
        "-m", "--max_verbs",
        help="number of verbs to print",
        type=int,
        default=200
    )
    parser.add_argument(
        "--no_magic",
        help="don't count verbs in magic methods",
        action="store_true",
        default=False
    )
    return parser.parse_args()


def walk_project(project_dir, parser, analyzer):
    results = {}
    for root, dirs, files in os.walk(project_dir, topdown=True):
        for file in files:
            parsed_data = parser.process(file)
            results[file] = analyzer.process(parsed_data)
    return results


def count_part_of_speech(projects):
    class PythonFuncNameParser(ExtractWordsFromFuncNamesMixin, PythonParser):
        pass

    class PartOfSpeechCounter(FilterPartOfSpeechMixin, Analyzer):
        pass

    python_func_name_parser = PythonFuncNameParser()
    part_of_speech_counter = PartOfSpeechCounter("verb")  # TODO: подставить из args
    statistics = {}
    for project in projects:
        if not os.path.isdir(project):
            continue
        statistics[project] = walk_project(project, python_func_name_parser, part_of_speech_counter)


if __name__ == "__main__":
    args = parse_cmd_line_args()
    projects = args.projects
    if args.projects_list:
        with open(args.projects_list) as fp:
            projects.extend(map(str.strip, fp.readlines()))
    projects = [os.path.join(args.dir, project) for project in projects]


