from mindee.parsing.common.ocr.mvision_v1 import MVisionV1
from mindee.parsing.common.string_dict import StringDict


class Ocr:
    """OCR extraction from the entire document."""

    mvision_v1: MVisionV1
    """Mindee Vision v1 results."""

    def __init__(self, raw_prediction: StringDict) -> None:
        self.mvision_v1 = MVisionV1(raw_prediction["mvision-v1"])

    def __str__(self) -> str:
        return str(self.mvision_v1)
