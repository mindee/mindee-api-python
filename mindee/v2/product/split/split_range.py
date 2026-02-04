from typing import List

from mindee.parsing.common.string_dict import StringDict


class SplitRange:
    """Split inference result."""

    page_range: List[int]
    """Page range of the split inference."""
    document_type: str
    """Document type of the split inference."""

    def __init__(self, server_response: StringDict):
        self.page_range = server_response["page_range"]
        self.document_type = server_response["document_type"]

    def __str__(self) -> str:
        page_range = ",".join([str(page_index) for page_index in self.page_range])
        return f"* :Page Range: {page_range}\n  :Document Type: {self.document_type}"
