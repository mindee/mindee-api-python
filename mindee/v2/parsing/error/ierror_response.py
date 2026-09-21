from typing import Protocol

from mindee.v2.parsing.error.error_item import ErrorItem


class IErrorResponse(Protocol):
    """Error response detailing a problem. The format adheres to RFC 9457."""

    status: int
    """The HTTP status code returned by the server."""

    detail: str
    """A human-readable explanation specific to the occurrence of the problem."""

    title: str
    """A short, human-readable summary of the problem."""

    code: str
    """A machine-readable code specific to the occurrence of the problem."""

    errors: list[ErrorItem]
    """A list of explicit details on the problem."""
