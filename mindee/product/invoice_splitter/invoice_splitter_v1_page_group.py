from typing import List

from mindee.parsing.common import StringDict


class InvoiceSplitterV1PageGroup:
    """Pages indexes in a group for Invoice Splitter V1."""

    page_indexes: List[int]
    """Index of each page"""
    confidence: float
    """Confidence score"""

    def __init__(self, raw_prediction: StringDict) -> None:
        self.page_indexes = raw_prediction["page_indexes"]
        try:
            self.confidence = float(raw_prediction["confidence"])
        except (KeyError, TypeError):
            self.confidence = 0.0

    def __str__(self) -> str:
        return f":Page indexes: {', '.join([str(page_index) for page_index in self.page_indexes])}"
