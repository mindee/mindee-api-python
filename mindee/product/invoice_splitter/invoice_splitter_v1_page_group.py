from typing import List

from mindee.parsing.common.api_response import StringDict

class InvoiceSplitterV1PageGroup:
    """Pages indexes in a group for Invoice Splitter V1."""

    page_indexes: List[int] = []
    """Index of each page"""
    confidence: float = 0.0
    """Confidence score"""

    def __init__(self, prediction: StringDict):
        self.page_indexes = prediction["page_indexes"]
        try:
            self.confidence = float(prediction["confidence"])
        except (KeyError, TypeError):
            pass

    def __str__(self) -> str:
        return f":Page indexes: {', '.join([str(page_index) for page_index in self.page_indexes])}"
