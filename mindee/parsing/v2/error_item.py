from typing import Optional

from mindee.parsing.common.string_dict import StringDict


class ErrorItem:
    """Explicit details on a problem."""

    pointer: Optional[str]
    """A JSON Pointer to the location of the body property."""
    detail: str
    """Explicit information on the issue."""

    def __init__(self, raw_response: StringDict):
        self.pointer = raw_response.get("pointer", None)
        self.detail = raw_response["detail"]
