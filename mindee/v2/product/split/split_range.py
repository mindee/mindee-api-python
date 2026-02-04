from typing import List

from mindee.parsing.common.string_dict import StringDict


class SplitRange:
    """Split inference result."""

    page_range: List[int]
    """
    0-based page indexes, where the first integer indicates the start page and the
    second integer indicates the end page.
    """
    document_type: str
    """The document type, as identified on given classification values."""

    def __init__(self, server_response: StringDict):
        self.page_range = server_response["page_range"]
        self.document_type = server_response["document_type"]

    def __str__(self) -> str:
        page_range = ",".join([str(page_index) for page_index in self.page_range])
        return f"* :Page Range: {page_range}\n  :Document Type: {self.document_type}"
