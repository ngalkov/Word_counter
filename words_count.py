"""Collect verb usage statistics through projects"""


import os
import argparse
from collections import Counter

from utils import *
import python_parsing
from natural_language_processing import PartOfSpeechFilter


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


def count_part_of_speech_python(projects):
    class FuncNameParser(python_parsing.ExtractWordsFromFuncNamesMixin, python_parsing.Parser):
        pass
    words_statistics = Counter()
    words_count = 0
    func_name_parser = FuncNameParser()
    part_of_speech_counter = PartOfSpeechFilter(["verb", "noun"])  # TODO: подставить из args
    for project in projects:
        if not os.path.isdir(project):
            continue
        for file in walk_dir(project):
            parsed_data = func_name_parser.process(file)
            words = part_of_speech_counter.process(parsed_data)
            words_statistics.update(words)
            words_count += len(words)
    return words_statistics, words_count


if __name__ == "__main__":
    args = parse_cmd_line_args()
    projects = args.projects
    if args.projects_list:
        with open(args.projects_list) as fp:
            projects.extend(map(str.strip, fp.readlines()))
    projects = [os.path.join(args.dir, project) for project in projects]
