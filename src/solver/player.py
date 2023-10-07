from typing import Dict

from src.solver.algorithmv2 import Algorithm, CharProbability, CharProbabilityWithWiki
from src.dataset.dataset import DatasetReader


class Player:
    _MAX_CHARACTERS: int = 26
    _LIST_OF_ALGORITHMS = {
        "char_prob": CharProbability(),
        # "wiki":  CharProbabilityWithWiki()
    }

    def __init__(self, algorithms=None) -> None:
        if algorithms is None:
            algorithms = self._LIST_OF_ALGORITHMS
        self._algorithms: Dict[str, Algorithm] = algorithms
        self._words_by_length = DatasetReader.read_english_words_dataset()

    def restart(self):
        for algorithm_name in self._algorithms:
            self._algorithms[algorithm_name].restart()

    def play(self, progress) -> Dict:
        filtered_words = self.get_words(progress)
        suggestions = {algorithm_name: self._algorithms[algorithm_name].play(filtered_words, progress)
                       for algorithm_name in self._algorithms}
        return suggestions

    def get_words(self, progress):
        if len(progress) not in self._words_by_length:
            raise f"Unexpected length of {len(progress)}"
        return [word for word in self._words_by_length[len(progress)] if self._is_match(word, progress)]

    @staticmethod
    def _is_match(word, progress) -> bool:
        """
        :param word: the word to test
        :param progress: the current progress with _ in unknown words e.g. "_u__"
        :return:
        """
        for w, p in zip(word, progress):
            if p != '_' and p != w:
                return False
        return True


