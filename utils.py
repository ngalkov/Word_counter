import os


def walk_dir(dir_path):
    for root, dirs, files in os.walk(dir_path, topdown=True):
        for file in files:
            yield file


def read_file(file_path):
    """Return file content or None in case of error"""
    try:
        with open(file_path) as fp:
            return fp.read()
    except OSError:
        return None


def split_snake_case_to_words(name):
    return [word for word in name.split('_') if word]
