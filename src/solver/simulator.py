from itertools import groupby
from typing import List, Tuple

import pandas as pd

from src.solver.algorithmv2 import CharProbability, CharProbabilityWithWiki
from src.dataset.dataset import DatasetReader
from src.solver.player import Player


class Report:
    _MAX_MISTAKES: int = 8

    def __init__(self, data: List[Tuple[str, str, int]], test_words: List[str], algorithm_names: List[str]) -> None:
        """
        :param data: (algorithm_name, word, number of mistakes)
        """
        self._test_words = test_words
        self._algorithm_names = algorithm_names

        pd.options.display.float_format = '{:,.2f}'.format
        self.rawdata = data
        self.dataframe = self._generate_dataframe()
        self.stats = self._generate_stats()

    def _generate_dataframe(self) -> pd.DataFrame:
        # rawdata_dict = {entry[1]: (entry[0], entry[2]) for entry in self.rawdata}
        sorted_entries = sorted(self.rawdata, key=lambda x: x[1])
        grouped_entries = {k: {g[0]: g[2] for g in list(group)} for k, group in groupby(sorted_entries, key=lambda x: x[1])}
        converted_data = []
        for word in grouped_entries:
            entry = [word]
            for algorithm_name in self._algorithm_names:
                entry.append(grouped_entries[word][algorithm_name])
            converted_data.append(entry)
        return pd.DataFrame(converted_data, columns=["word"] + self._algorithm_names)

    @staticmethod
    def _n_failed(data: List[int]):
        return sum([1 if d >= Report._MAX_MISTAKES else 0 for d in data])

    @staticmethod
    def _n_success(data: List[int]):
        return sum([1 if d < Report._MAX_MISTAKES else 0 for d in data])

    def _failure_rate(self, data: List[int]):
        n_fail = Report._n_failed(data)
        return float(n_fail) / float(len(self._test_words))

    def _success_rate(self, data: List[int]):
        n_success = Report._n_success(data)
        return float(n_success) / float(len(self._test_words))

    @staticmethod
    def _min_mistakes_per_word(data: List[int]):
        return min(data)

    @staticmethod
    def _max_mistakes_per_word(data: List[int]):
        return max(data)

    def _n_test_words(self, data: List[int]):
        return len(self._test_words)

    def _generate_stats(self):
        stats_rows = []
        funcs = [self._n_test_words, Report._min_mistakes_per_word, Report._max_mistakes_per_word, Report._n_failed, Report._n_success, self._failure_rate, self._success_rate]
        for func in funcs:
            row = [func.__name__]
            for algorithm_name in self._algorithm_names:
                dataset = list(self.dataframe[algorithm_name])
                row.append(func(dataset))
            stats_rows.append(row)
        return pd.DataFrame(stats_rows, columns=["Func"] + self._algorithm_names)


class Simulator:
    _LIST_OF_ALGORITHMS = {
        # "rand_guess": RandomGuess(),
        "char_prob": CharProbability(),
        "wiki_100000": CharProbabilityWithWiki(divider=10000),
        "wiki_10000": CharProbabilityWithWiki(divider=1000),
    }
    _TEST_WORDS: List[str] = ["book", "pumpkin", "moldova", "radiohead",
                              "cuttlefish", "ice", "cat", "dog", "life", "protagonist",
                              "worldwide", "egypt", "zugtierlaster"] + DatasetReader.random_english_words()

    def __init__(self, debug: bool = False) -> None:
        self._debug = debug

    def _log(self, message):
        if self._debug:
            print(message)

    def simulate(self) -> Report:
        self._log("Start simulator")
        report_data = []
        for algorithm_name in self._LIST_OF_ALGORITHMS:
            for word in self._TEST_WORDS:
                mistakes = self._run_test_word(word, algorithm_name)
                self._log((algorithm_name, word, mistakes))
                report_data.append((algorithm_name, word, mistakes))
                print((algorithm_name, word, mistakes))
        return Report(report_data, self._TEST_WORDS, list(self._LIST_OF_ALGORITHMS.keys()))

    def _run_test_word(self, word, algorithm_name):
        self._log(f"Running {word}, {algorithm_name}")
        player = Player(algorithms={algorithm_name: self._LIST_OF_ALGORITHMS[algorithm_name]})
        player.restart()
        progress = "_" * len(word)
        n_mistakes = 0
        while "_" in progress:
            results = player.play(progress)
            char_suggestion = results[algorithm_name]
            if char_suggestion is None:
                break
            char_suggestion = char_suggestion[0]
            if char_suggestion in word:
                progress = self._update_progress(word, progress, char_suggestion)
            else:
                n_mistakes += 1
            self._log((word, char_suggestion, progress))
        return n_mistakes

    @staticmethod
    def _update_progress(word, progress, char_suggestion):
        new_progress = progress
        for i in range(len(word)):
            if char_suggestion == word[i]:
                new_progress = new_progress[:i] + char_suggestion + new_progress[i + 1:]
        return new_progress
