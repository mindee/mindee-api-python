import json
from abc import ABC

from mindee.logger import logger
from mindee.parsing.common.api_request import ApiRequest
from mindee.parsing.common.string_dict import StringDict


class ApiResponse(ABC):
    """
    Base class for responses sent by the server.

    Serves as a base class for responses to both synchronous and asynchronous calls.
    """

    api_request: ApiRequest
    """Results of the request sent to the API."""
    _raw_http: StringDict
    """Raw request sent by the server, as a dict."""

    def __init__(self, raw_response: StringDict) -> None:
        logger.debug("Handling API response")
        self.api_request = ApiRequest(raw_response["api_request"])
        self._raw_http = raw_response

    @property
    def raw_http(self) -> str:
        """Displays the result of the raw response as json string."""
        return json.dumps(self._raw_http, indent=2)
