from typing import List

from mindee.geometry.minmax import get_min_max_x
from mindee.parsing.common.ocr.ocr_word import OcrWord


class OcrLine(List[OcrWord]):
    """A list of words which are on the same line."""

    def sort_on_x(self) -> None:
        """Sort the words on the line from left to right."""
        self.sort(key=lambda item: get_min_max_x(item.polygon).min)

    def __str__(self) -> str:
        return " ".join([word.text for word in self])
