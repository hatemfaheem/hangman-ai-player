import os
from itertools import groupby
import random
from typing import Dict, List


class DatasetReader:
    _wiki: Dict[str, int] = None
    _words_by_length: Dict[int, List[str]] = None
    _english_words: List[str] = None

    @staticmethod
    def read_english_words_dataset() -> Dict[int, List[str]]:
        if DatasetReader._words_by_length is not None:
            return DatasetReader._words_by_length
        DatasetReader._english_words = DatasetReader.read_english_words_as_list()
        DatasetReader._words_by_length = {k: list(group) for k, group in groupby(DatasetReader._english_words, key=len)}
        return DatasetReader._words_by_length

    @staticmethod
    def read_english_words_as_list() -> List[str]:
        os.chdir("/Users/hatem/Workspace/Hangman")
        if DatasetReader._english_words is not None:
            return DatasetReader._english_words
        with open("/Users/hatem/Workspace/Hangman/src/dataset/data/added_words.txt") as file:
            added_words = [DatasetReader._preprocess(line) for line in file.readlines()]
        with open("/Users/hatem/Workspace/Hangman/src/dataset/data/all_english_words.txt") as file:
            english_words = [DatasetReader._preprocess(line) for line in file.readlines()]
        DatasetReader._english_words = sorted(list(set(english_words + added_words)), key=lambda x: len(x))
        return DatasetReader._english_words

    @staticmethod
    def random_english_words(sample_size=100) -> List[str]:
        DatasetReader._english_words = DatasetReader.read_english_words_as_list()
        return random.sample(DatasetReader._english_words, sample_size)

    @staticmethod
    def read_wiki_word_freq_dataset() -> Dict[str, int]:
        if DatasetReader._wiki is not None:
            return DatasetReader._wiki
        with open("/Users/hatem/Workspace/Hangman/src/dataset/data/enwiki-20210820-words-frequency.txt") as file:
            wiki_lines = [line.split() for line in file.readlines()]
            wiki_words = {DatasetReader._preprocess(line[0]): int(line[1]) for line in wiki_lines}
        DatasetReader._wiki = wiki_words
        return wiki_words

    @staticmethod
    def _preprocess(line):
        return line.rstrip().lower()
