import random
import string
from collections import Counter
from math import ceil
from typing import List, Tuple

from src.dataset.dataset import DatasetReader
from abc import abstractmethod

_MAX_CHARACTERS = 26


class Algorithm:
    def __init__(self) -> None:
        self._suggested = set()

    def restart(self):
        self._suggested = set()

    def play(self, filtered_words: List, progress: str) -> (str, int):
        char_prob = self._calculate_character_probability(filtered_words)
        try:
            suggestion = next(c for c in char_prob if c[0] not in self._suggested)
        except StopIteration:
            return None
        self._suggested.add(suggestion[0])
        return suggestion

    @abstractmethod
    def _calculate_character_probability(self, filtered_words) -> List[Tuple[str, int]]:
        """
        Return a list of characters ordered by priority
        """
        pass


class CharProbability(Algorithm):
    def _calculate_character_probability(self, filtered_words):
        all_chars_in_dataset = [char for word in filtered_words for char in word]  # flat map
        char_prob = Counter({c: 0 for c in string.ascii_lowercase})
        char_prob.update(all_chars_in_dataset)
        assert len(char_prob) == _MAX_CHARACTERS, f"Expected exactly {_MAX_CHARACTERS} characters."
        return char_prob.most_common()


class RandomGuess(Algorithm):
    def _calculate_character_probability(self, filtered_words):
        char_prob = Counter({c: -1 for c in string.ascii_lowercase})
        assert len(char_prob) == _MAX_CHARACTERS, f"Expected exactly {_MAX_CHARACTERS} characters."
        results = char_prob.most_common()
        random.shuffle(results)
        return results


class CharProbabilityWithWiki(Algorithm):
    def __init__(self, divider=1000) -> None:
        super(CharProbabilityWithWiki, self).__init__()
        self._wiki = DatasetReader.read_wiki_word_freq_dataset()
        self._divider = divider

    def _calculate_character_probability(self, filtered_words) -> List:
        all_chars_in_dataset_with_word_freq = [char*ceil(self._wiki.get(word, 1)/self._divider) for word in filtered_words for char in word]
        all_chars_in_dataset = [char for word in all_chars_in_dataset_with_word_freq for char in word]
        char_prob = Counter({c: 0 for c in string.ascii_lowercase})
        char_prob.update(all_chars_in_dataset)
        assert len(char_prob) == _MAX_CHARACTERS, f"Expected exactly {_MAX_CHARACTERS} characters."
        return char_prob.most_common()
