"""Utils for process natural language"""

import re
import abc
import itertools

from nltk import pos_tag

# Word tags are part of the corpus. By default it's Penn Treebank Tag Set:
# http://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
# see also https://stackoverflow.com/questions/15388831/what-are-all-possible-pos-tags-of-nltk
PART_OF_SPEECH_PATTERNS = {
    "verb": "VB[DGNPZ]?$",
    "noun": "NN(PS|S|P)?$",
}


class BaseAnalyzer(abc.ABC):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @abc.abstractmethod
    def process(self, data):
        pass


class PartOfSpeechFilter(BaseAnalyzer):
    """Filter words list by part of speech matching"""
    def __init__(self, part_of_speech_list, **kwargs):
        self.part_of_speech_list = part_of_speech_list
        super().__init__(**kwargs)

    def process(self, words):
        return [word for word in words if tag_part_of_speech(word) in self.part_of_speech_list]


def tag_part_of_speech(word):
    """Return part of speech for word or None if word can't be tagged"""
    if not word:
        return None
    pos_info = pos_tag([word])
    word_tag = pos_info[0][1]
    for part_of_speech, pattern in PART_OF_SPEECH_PATTERNS:
        if re.match(pattern, word_tag):
            return part_of_speech
    return None
