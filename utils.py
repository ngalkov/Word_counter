import os
import subprocess
from urllib.parse import urlparse


def walk_dir(dir_path):
    for root, dirs, files in os.walk(dir_path, topdown=True):
        for file in files:
            yield os.path.join(root, file)


def read_file(file_path):
    """Return file content or None in case of error"""
    try:
        with open(file_path) as fp:
            return fp.read()
    except OSError:
        return None


def is_path_remote(path):
    url_components = urlparse(path)
    if all([url_components.scheme, url_components.netloc]):
        return True
    return False


def split_snake_case_to_words(name):
    return [word for word in name.split('_') if word]


def fetch_remote_repo(repo_url, target_dir="./"):
    try:
        subprocess.run(["git", "clone", str(repo_url), str(target_dir)], timeout=100, check=True)
    except (OSError, subprocess.CalledProcessError):
        pass
