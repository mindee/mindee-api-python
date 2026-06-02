from mindee.parsing.common.string_dict import StringDict
from mindee.v1.parsing.common.ocr.ocr_page import OCRPage


class MVisionV1:
    """Mindee Vision V1."""

    pages: list[OCRPage]
    """List of pages."""

    def __init__(self, raw_prediction: StringDict) -> None:
        self.pages = [
            OCRPage(page_prediction) for page_prediction in raw_prediction["pages"]
        ]

    def __str__(self) -> str:
        return "\n".join([str(page) for page in self.pages])
