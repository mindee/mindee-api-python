from typing import List

from mindee.parsing.common.string_dict import StringDict
from mindee.v2.product.ocr.ocr_word import OCRWord


class OCRPage:
    """OCR result for a single page."""

    words: List[OCRWord]
    """List of words extracted from the document page."""
    content: str
    """Full text content extracted from the document page."""

    def __init__(self, raw_response: StringDict) -> None:
        self.words = [OCRWord(word) for word in raw_response["words"]]
        self.content = raw_response["content"]

    def __str__(self) -> str:
        ocr_words = "\n"
        if len(self.words) > 0:
            ocr_words += "\n\n".join([str(word) for word in self.words])
        out_str = f"OCR Words\n======{ocr_words}"
        out_str += f"\n\n:Content: {self.content}"
        return out_str
