from src.android.screen_reader import ScreenReader
from src.android.touch_bot import TouchBot
from src.solver.player import Player
from src.vision.level_scanner import LevelScanner


class GameManager:
    ALGORITHM_NAME = "char_prob"

    def __init__(self) -> None:
        self.screen_reader = ScreenReader()
        self.level_scanner = LevelScanner()
        self.player = Player()
        self.touch_bot = TouchBot()

    def game_loop(self):
        prev_progress = None
        suggestion = None
        while True:
            image = self.screen_reader.read_level_image()
            obsrv_progress = self.level_scanner.scan(image)
            # print(f"observation: {obsrv_progress}")
            prev_progress = self.update_progress(prev_progress, obsrv_progress, suggestion)
            print(f"progress: {prev_progress}")
            suggestion = self.player.play(prev_progress)[self.ALGORITHM_NAME][0]
            print(f"suggestion: {suggestion}")
            self.touch_bot.suggest_character(suggestion)

    @staticmethod
    def update_progress(previous_progress, obsrv_progress, suggestion):
        if previous_progress is None:
            return obsrv_progress
        new_progress = ""
        for i in range(len(obsrv_progress)):
            if obsrv_progress[i] == 'X':
                if previous_progress[i] == '_':
                    new_progress += suggestion
                else:
                    new_progress += previous_progress[i]
            else:
                new_progress += "_"
        return new_progress
