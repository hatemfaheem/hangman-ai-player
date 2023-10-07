from typing import List, Tuple

import cv2
import numpy as np


def render(img):
    cv2.imshow("render", img)
    cv2.waitKey(0)


class LevelScanner:
    # Finding the contours
    CONTOUR_SIZE_THRESHOLD: int = 40
    HEIGHT_OFFSET: int = 1470
    WORD_AREA_HEIGHT: int = 150

    # splitting characters from dashes
    HORIZONTAL_THRESHOLD: int = HEIGHT_OFFSET + 100

    # assigning characters to dashes
    VERTICAL_THRESHOLD: int = 25

    SPACE_THRESHOLD: int = 180

    @staticmethod
    def crop_word_part(img):
        y, h, x, w = LevelScanner.HEIGHT_OFFSET, LevelScanner.WORD_AREA_HEIGHT, 0, img.shape[1]
        return img[y:y + h, x:x + w]

    def scan_from_path(self, file_path, debug=False):
        original_img = cv2.imread(file_path)
        return self.scan(original_img, debug)

    def scan(self, original_img, debug=False):
        img = self.crop_word_part(original_img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh1 = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        img = cv2.dilate(thresh1, rect_kernel, iterations=1)
        contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        centers = []
        cv2.line(original_img, (0, LevelScanner.HORIZONTAL_THRESHOLD), (original_img.shape[1], LevelScanner.HORIZONTAL_THRESHOLD), (0, 255, 0), thickness=5)
        for contour in contours:
            center = np.mean(contour, axis=0).tolist()[0]
            center = (int(center[0]), int(center[1]+LevelScanner.HEIGHT_OFFSET))
            if contour.size >= LevelScanner.CONTOUR_SIZE_THRESHOLD:
                cv2.circle(original_img, center, 10, (0, 0, 255), 3)
                centers.append(center)
        dashes, chars = self.post_process(centers)
        level_progress = self.assign_characters_to_dashes(dashes, chars)
        level_progress = self.inject_space_if_any(dashes, level_progress)
        if debug:
            render(original_img)
        return level_progress

    def _is_dash(self, center):
        return center[1] >= self.HORIZONTAL_THRESHOLD

    def post_process(self, centers: List[Tuple[int, int]]):
        dashes = sorted([c for c in centers if self._is_dash(c)], key=lambda x: x[0])
        chars = sorted([c for c in centers if not self._is_dash(c)], key=lambda x: x[0])
        return dashes, chars

    def _belongs(self, dash, char):
        return abs(char[0] - dash[0]) <= self.VERTICAL_THRESHOLD

    def assign_characters_to_dashes(self, dashes, chars):
        level_progress = "_" * len(dashes)
        for i in range(len(dashes)):
            dash = dashes[i]
            for char in chars:
                if self._belongs(dash, char):
                    level_progress = level_progress[:i] + "X" + level_progress[i + 1:]
        return level_progress

    def inject_space_if_any(self, dashes, level_progress):
        index_of_space = -1
        for i in range(1, len(dashes)):
            if dashes[i][0] - dashes[i - 1][0] >= self.SPACE_THRESHOLD:
                index_of_space = i
                break
        if index_of_space == -1:
            return level_progress
        return level_progress[:index_of_space] + " " + level_progress[index_of_space:]
