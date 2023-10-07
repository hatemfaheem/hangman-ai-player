import os
import time


class TouchBot:
	ADB_PATH: str = "/Users/hatem/Downloads/software/platform-tools/adb"
	CHAR_LOCATIONS = {
		"a": (103, 1891),
		"b": (341, 1881),
		"c": (529, 1879),
		"d": (725, 1890),
		"e": (922, 1873),
		"f": (1092, 1896),
		"g": (1311, 1882),
		"h": (139, 2098),
		"i": (331, 2119),
		"j": (526, 2106),
		"k": (727, 2087),
		"l": (899, 2096),
		"m": (1116, 2108),
		"n": (1295, 2132),
		"o": (135, 2321),
		"p": (361, 2325),
		"q": (559, 2329),
		"r": (736, 2336),
		"s": (927, 2304),
		"t": (1118, 2288),
		"u": (1305, 2300),
		"v": (350, 2520),
		"w": (554, 2514),
		"x": (737, 2502),
		"y": (927, 2490),
		"z": (1099, 2499),
	}

	def suggest_character(self, suggestion):
		if suggestion not in self.CHAR_LOCATIONS:
			raise f"Wrong character suggestion: '{suggestion}'"
		self._emulate_touch(self.CHAR_LOCATIONS[suggestion][0], self.CHAR_LOCATIONS[suggestion][1])
		time.sleep(1)

	@staticmethod
	def _emulate_touch(x, y):
		os.system(f"{TouchBot.ADB_PATH} shell input tap {x} {y}")