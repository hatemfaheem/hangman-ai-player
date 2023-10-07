import time

from src.android.touch_bot import TouchBot

if __name__ == '__main__':
    touch_bot = TouchBot()
    chars = ["w", "x", "y", "z"]
    for char in chars:
        print(f"Touching {char}")
        touch_bot.suggest_character(char)
        time.sleep(1)
