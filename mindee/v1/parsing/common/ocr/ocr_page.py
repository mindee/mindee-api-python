from mindee.geometry.minmax import get_min_max_y
from mindee.geometry.polygon import is_point_in_polygon_y
from mindee.geometry.polygon_utils import get_centroid
from mindee.parsing.common.string_dict import StringDict
from mindee.v1.parsing.common.ocr.ocr_line import OCRLine
from mindee.v1.parsing.common.ocr.ocr_word import OCRWord


class OCRPage:
    """OCR extraction for a single page."""

    _all_words: list[OCRWord]
    _lines: list[OCRLine]

    def __init__(self, raw_prediction: StringDict) -> None:
        self._all_words = [
            OCRWord(word_prediction) for word_prediction in raw_prediction["all_words"]
        ]
        # make sure words are sorted from top to bottom
        self._all_words.sort(
            key=lambda item: get_min_max_y(item.polygon).min, reverse=False
        )
        self._lines = []

    @staticmethod
    def _are_words_on_same_line(current_word: OCRWord, next_word: OCRWord) -> bool:
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

    def _to_lines(self) -> list[OCRLine]:
        """Order all the words on the page into lines."""
        current: OCRWord | None = None
        indexes: list[int] = []
        lines: list[OCRLine] = []

        for _ in self._all_words:
            line: OCRLine = OCRLine()
            for idx, word in enumerate(self._all_words):
                if idx in indexes:
                    continue
                if current is None:
                    current = word
                    indexes.append(idx)
                    line = OCRLine()
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
    def all_lines(self) -> list[OCRLine]:
        """All the words on the page, ordered in lines."""
        if not self._lines:
            self._lines = self._to_lines()
        return self._lines

    @property
    def all_words(self) -> list[OCRWord]:
        """All the words on the page, in semi-random order."""
        return self._all_words

    def __str__(self) -> str:
        return "\n".join(str(line) for line in self.all_lines) + "\n"
