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

    def __init__(self, json_response: dict) -> None:
        self.url = json_response["url"]
        self.error = json_response["error"]
        self.resources = json_response["resources"]
        self.status = RequestStatus(json_response["status"])
        self.status_code = json_response["status_code"]
