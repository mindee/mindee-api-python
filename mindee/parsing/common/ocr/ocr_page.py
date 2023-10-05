from typing import List, Optional

from mindee.geometry.minmax import get_min_max_y
from mindee.geometry.polygon import is_point_in_polygon_y
from mindee.geometry.polygon_utils import get_centroid
from mindee.parsing.common.ocr.ocr_line import OcrLine
from mindee.parsing.common.ocr.ocr_word import OcrWord
from mindee.parsing.common.string_dict import StringDict


class OcrPage:
    """OCR extraction for a single page."""

    _all_words: List[OcrWord]
    _lines: List[OcrLine]

    def __init__(self, raw_prediction: StringDict) -> None:
        self._all_words = [
            OcrWord(word_prediction) for word_prediction in raw_prediction["all_words"]
        ]
        # make sure words are sorted from top to bottom
        self._all_words.sort(
            key=lambda item: get_min_max_y(item.polygon).min, reverse=False
        )
        self._lines = []

    @staticmethod
    def _are_words_on_same_line(current_word: OcrWord, next_word: OcrWord) -> bool:
        """Determine if two words are on the same line."""
        current_in_next = is_point_in_polygon_y(
            get_centroid(current_word.polygon),
            next_word.polygon,
        )
        next_in_current = is_point_in_polygon_y(
            get_centroid(next_word.polygon), current_word.polygon
        )
        # We need to check both to eliminate any issues due to word order.
        return current_in_next or next_in_current

    def _to_lines(self) -> List[OcrLine]:
        """Order all the words on the page into lines."""
        current: Optional[OcrWord] = None
        indexes: List[int] = []
        lines: List[OcrLine] = []

        for _ in self._all_words:
            line: OcrLine = OcrLine()
            for idx, word in enumerate(self._all_words):
                if idx in indexes:
                    continue
                if current is None:
                    current = word
                    indexes.append(idx)
                    line = OcrLine()
                    line.append(word)
                else:
                    if self._are_words_on_same_line(current, word):
                        line.append(word)
                        indexes.append(idx)
            current = None
            if line:
                line.sort_on_x()
                lines.append(line)
        return lines

    @property
    def all_lines(self) -> List[OcrLine]:
        """All the words on the page, ordered in lines."""
        if not self._lines:
            self._lines = self._to_lines()
        return self._lines

    @property
    def all_words(self) -> List[OcrWord]:
        """All the words on the page, in semi-random order."""
        return self._all_words

    def __str__(self) -> str:
        return "\n".join(str(line) for line in self.all_lines) + "\n"
