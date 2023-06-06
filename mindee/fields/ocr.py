from typing import List, Optional

from mindee.documents.base import TypeApiPrediction
from mindee.geometry import (
    Polygon,
    get_centroid,
    get_min_max_x,
    get_min_max_y,
    is_point_in_polygon_y,
    polygon_from_prediction,
)


class Word:
    """A single word."""

    confidence: float
    polygon: Polygon
    text: str

    def __init__(self, prediction: TypeApiPrediction):
        self.confidence = prediction["confidence"]
        self.polygon = polygon_from_prediction(prediction["polygon"])
        self.text = prediction["text"]

    def __str__(self) -> str:
        return self.text


class OcrLine(List[Word]):
    """A list of words which are on the same line."""

    def sort_on_x(self) -> None:
        """Sort the words on the line from left to right."""
        self.sort(key=lambda item: get_min_max_x(item.polygon).min)

    def __str__(self) -> str:
        return " ".join([word.text for word in self])


class OcrPage:
    """OCR extraction for a single page."""

    all_words: List[Word]
    """All the words on the page, in semi-random order."""
    _lines: List[OcrLine]

    def __init__(self, prediction: TypeApiPrediction):
        self.all_words = [
            Word(word_prediction) for word_prediction in prediction["all_words"]
        ]
        self._lines = []

    @staticmethod
    def _are_words_on_same_line(current_word: Word, next_word: Word) -> bool:
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
        current: Optional[Word] = None
        indexes: List[int] = []
        lines: List[OcrLine] = []

        # make sure words are sorted from top to bottom
        self.all_words.sort(
            key=lambda item: get_min_max_y(item.polygon).min, reverse=False
        )

        for _ in self.all_words:
            line: OcrLine = OcrLine()
            for idx, word in enumerate(self.all_words):
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

    def __str__(self) -> str:
        return "\n".join(str(line) for line in self.all_lines) + "\n"


class MVisionV1:
    """Mindee Vision V1."""

    pages: List[OcrPage]

    def __init__(self, prediction: TypeApiPrediction):
        self.pages = [
            OcrPage(page_prediction) for page_prediction in prediction["pages"]
        ]

    def __str__(self) -> str:
        return "\n".join([str(page) for page in self.pages])


class Ocr:
    """OCR extraction from the entire document."""

    mvision_v1: MVisionV1

    def __init__(self, prediction: TypeApiPrediction):
        self.mvision_v1 = MVisionV1(prediction["mvision-v1"])

    def __str__(self) -> str:
        return str(self.mvision_v1)
