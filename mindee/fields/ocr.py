from typing import List, Optional

from mindee.documents.base import TypeApiPrediction
from mindee.fields.base import FieldPositionMixin
from mindee.geometry import (
    get_centroid,
    get_min_max_x,
    get_min_max_y,
    is_point_in_polygon_y,
)


class OcrWord(FieldPositionMixin):
    """A single word."""

    confidence: float
    """The confidence score."""
    text: str
    """The extracted text."""

    def __init__(self, prediction: TypeApiPrediction):
        self.confidence = prediction["confidence"]
        self.text = prediction["text"]
        self._set_position(prediction)

    def __str__(self) -> str:
        return self.text


class OcrLine(List[OcrWord]):
    """A list of words which are on the same line."""

    def sort_on_x(self) -> None:
        """Sort the words on the line from left to right."""
        self.sort(key=lambda item: get_min_max_x(item.polygon).min)

    def __str__(self) -> str:
        return " ".join([word.text for word in self])


class OcrPage:
    """OCR extraction for a single page."""

    _all_words: List[OcrWord]
    _lines: List[OcrLine]

    def __init__(self, prediction: TypeApiPrediction):
        self._all_words = [
            OcrWord(word_prediction) for word_prediction in prediction["all_words"]
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


class MVisionV1:
    """Mindee Vision V1."""

    pages: List[OcrPage]
    """List of pages."""

    def __init__(self, prediction: TypeApiPrediction):
        self.pages = [
            OcrPage(page_prediction) for page_prediction in prediction["pages"]
        ]

    def __str__(self) -> str:
        return "\n".join([str(page) for page in self.pages])


class Ocr:
    """OCR extraction from the entire document."""

    mvision_v1: MVisionV1
    """Mindee Vision v1 results."""

    def __init__(self, prediction: TypeApiPrediction):
        self.mvision_v1 = MVisionV1(prediction["mvision-v1"])

    def __str__(self) -> str:
        return str(self.mvision_v1)
