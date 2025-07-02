import json
from typing import Optional

from mindee.parsing.common.string_dict import StringDict


class MindeeHTTPErrorV2(RuntimeError):
    """An exception relating to HTTP calls."""

    status: int
    detail: Optional[str]

    def __init__(self, status: int, detail: Optional[str]) -> None:
        """
        Base exception for HTTP calls.

        :param status: HTTP code for the error
        :param detail: Error details.
        """
        self.status = status
        self.detail = detail
        super().__init__(f"HTTP error {status} - {detail}")


class MindeeHTTPUnknownErrorV2(MindeeHTTPErrorV2):
    """HTTP error with unknown status code."""

    def __init__(self, status: int, detail: Optional[str]) -> None:
        super().__init__(-1, f"Couldn't deserialize server error. Found: {detail}")


def handle_error_v2(json_response: StringDict) -> None:
    """
    Handles HTTP errors by raising MindeeHTTPErrorV2 exceptions with proper details.

    :raises MindeeHTTPErrorV2: If the response has been caught.
    :raises MindeeHTTPUnknownErrorV2: If the json return format is unreadable.
    """
    try:
        raise MindeeHTTPErrorV2(
            json_response["job"]["error"]["status"],
            json_response["job"]["error"]["detail"],
        )
    except Exception as exc:
        raise MindeeHTTPUnknownErrorV2(-1, json.dumps(json_response, indent=2)) from exc
