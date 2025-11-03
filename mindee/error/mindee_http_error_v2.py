import json
from typing import Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.v2 import ErrorItem, ErrorResponse


class MindeeHTTPErrorV2(RuntimeError, ErrorResponse):
    """An exception relating to HTTP calls."""

    def __init__(self, response: ErrorResponse) -> None:
        """
        Base exception for HTTP calls.

        :param response:
        """
        self.status = response.status
        self.title = response.title
        self.code = response.code
        self.detail = response.detail
        self.errors: list[ErrorItem] = response.errors
        super().__init__(
            f"HTTP {self.status} - {self.title} :: {self.code} - {self.detail}"
        )


class MindeeHTTPUnknownErrorV2(MindeeHTTPErrorV2):
    """HTTP error with unknown status code."""

    def __init__(self, detail: Optional[str]) -> None:
        super().__init__(
            ErrorResponse(
                {
                    "status": -1,
                    "code": "000-000",
                    "title": "Unknown Error",
                    "detail": f"Couldn't deserialize server error. Found: {detail}",
                }
            )
        )


def handle_error_v2(raw_response: StringDict) -> None:
    """
    Handles HTTP errors by raising MindeeHTTPErrorV2 exceptions with proper details.

    :raises MindeeHTTPErrorV2: If the response has been caught.
    :raises MindeeHTTPUnknownErrorV2: If the json return format is unreadable.
    """
    if "status" not in raw_response or "detail" not in raw_response:
        raise MindeeHTTPUnknownErrorV2(json.dumps(raw_response, indent=2))
    raise MindeeHTTPErrorV2(ErrorResponse(raw_response))
