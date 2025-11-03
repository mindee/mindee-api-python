from typing import List

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.v2.error_item import ErrorItem


class ErrorResponse:
    """Error response detailing a problem. The format adheres to RFC 9457."""

    status: int
    """The HTTP status code returned by the server."""
    detail: str
    """A human-readable explanation specific to the occurrence of the problem."""
    title: str
    """A short, human-readable summary of the problem."""
    code: str
    """A machine-readable code specific to the occurrence of the problem."""
    errors: List[ErrorItem]
    """A list of explicit error details."""

    def __init__(self, raw_response: StringDict):
        self.status = raw_response["status"]
        self.detail = raw_response["detail"]
        self.title = raw_response["title"]
        self.code = raw_response["code"]
        try:
            self.errors = [ErrorItem(error) for error in raw_response["errors"]]
        except KeyError:
            self.errors = []

    def __str__(self):
        return f"HTTP {self.status} - {self.title} :: {self.code} - {self.detail}"
