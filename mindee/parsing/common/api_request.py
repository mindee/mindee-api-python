from enum import Enum
from typing import List

from mindee.parsing.common.string_dict import StringDict


class RequestStatus(Enum):
    """Possible request statuses."""

    FAILURE = "failure"
    SUCCESS = "success"


class ApiRequest:
    """Information on the API request made to the server."""

    error: StringDict
    resources: List[str]
    status: RequestStatus
    status_code: int
    """HTTP status code."""
    url: str

    def __init__(self, raw_response: StringDict) -> None:
        self.url = raw_response["url"]
        self.error = raw_response["error"]
        self.resources = raw_response["resources"]
        self.status = RequestStatus(raw_response["status"])
        self.status_code = raw_response["status_code"]
