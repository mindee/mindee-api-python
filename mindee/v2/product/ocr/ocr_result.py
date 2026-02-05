from typing import List

from mindee.parsing.common.string_dict import StringDict
from mindee.v2.product.ocr.ocr_page import OCRPage


class OCRResult:
    """OCR result info."""

    pages: List[OCRPage]
    """List of OCR results for each page in the document."""

    def __init__(self, raw_response: StringDict) -> None:
        self.pages = [OCRPage(ocr) for ocr in raw_response["pages"]]

    def __str__(self) -> str:
        pages = "\n"
        if len(self.pages) > 0:
            pages += "\n\n".join([str(ocr) for ocr in self.pages])
        out_str = f"Pages\n======{pages}"
        return out_str
