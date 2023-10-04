from typing import List

from mindee.parsing.common.ocr.ocr_page import OcrPage
from mindee.parsing.common.string_dict import StringDict


class MVisionV1:
    """Mindee Vision V1."""

    pages: List[OcrPage]
    """List of pages."""

    def __init__(self, raw_prediction: StringDict) -> None:
        self.pages = [
            OcrPage(page_prediction) for page_prediction in raw_prediction["pages"]
        ]

    def __str__(self) -> str:
        return "\n".join([str(page) for page in self.pages])
