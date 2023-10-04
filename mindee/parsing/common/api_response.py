from abc import ABC

from mindee.logger import logger
from mindee.parsing.common.api_request import ApiRequest
from mindee.parsing.common.string_dict import StringDict


class ApiResponse(ABC):
    """
    Base class for responses sent by the server.

    Serves as a base class for responses to both synchronous and asynchronous calls.
    """

    raw_http: StringDict
    """Raw request sent by the server, as string."""

    def __init__(self, raw_response: StringDict) -> None:
        logger.debug("Handling API response")
        self.api_request = ApiRequest(raw_response["api_request"])
        self.raw_http = raw_response
