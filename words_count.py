"""Collect verb usage statistics through projects"""


import argparse
from collections import Counter

from utils import *
import python_parsing
from natural_language_processing import PartOfSpeechFilter, PART_OF_SPEECH_PATTERNS


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
        "-s", "--part_of_speech",
        help="part of speech to extract",
        choices=list(PART_OF_SPEECH_PATTERNS.keys()),
        nargs='+',
        default=list(PART_OF_SPEECH_PATTERNS.keys())
    )
    parser.add_argument(
        "-i", "--identifier",
        help="identifiers to extract",
        choices=list(python_parsing.NAME_EXTRACTION_MIXINS),
        nargs='+',
        default=list(python_parsing.NAME_EXTRACTION_MIXINS)
    )
    parser.add_argument(
        "-m", "--max_words",
        help="number of words to print",
        type=int,
        default=200
    )
    parser.add_argument(
        "--no_magic",
        help="don't count words in magic names",
        action="store_true",
        default=False
    )
    return parser.parse_args()


def extract_words_from_python_project(project_dir, python_ids, no_magic=False):
    """
    Return list of words, extracted from identifiers in python files from project_dir.

    :param project_dir: project directory
    :param python_ids: list of identifiers to extract from (e.g. ["func", "local_var"])
    :return: list of words
    """
    if not os.path.isdir(project_dir):
        return []
    # create parser for each identifier in python_ids
    parsers = []
    for python_id in python_ids:
        Mixin = python_parsing.NAME_EXTRACTION_MIXINS[python_id]

        class Parser(Mixin, python_parsing.Parser):
            pass
        parsers.append(Parser(no_magic=no_magic))

    words = []
    for file in walk_dir(project_dir):
        for parser in parsers:
            words.extend(parser.process(file))
    return words


def count_part_of_speech_in_python_projects(projects, python_ids, parts_of_speech, no_magic=False):
    part_of_speech_counter = PartOfSpeechFilter(parts_of_speech)
    words_statistics = Counter()
    for project in projects:
        words = extract_words_from_python_project(project, python_ids, no_magic=no_magic)
        filtered_words = part_of_speech_counter.process(words)
        words_statistics.update(filtered_words)
    return words_statistics


def make_report(words_statistics, max_words):
    words_count = sum(words_statistics.values())
    print('total %s words, %s unique' % (words_count, len(words_statistics)))
    for word, occurrence in words_statistics.most_common(max_words):
        print(word, occurrence)


if __name__ == "__main__":
    args = parse_cmd_line_args()
    projects = args.projects
    if args.projects_list:
        with open(args.projects_list) as fp:
            projects.extend(map(str.strip, fp.readlines()))
    projects = [os.path.join(args.dir, project) for project in projects]
    words_statistics = count_part_of_speech_in_python_projects(
        projects,
        args.identifier,
        args.part_of_speech,
        args.no_magic
    )
    make_report(words_statistics, args.max_words)