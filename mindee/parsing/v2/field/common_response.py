import json
from enum import Enum

from mindee.logger import logger
from mindee.parsing.common.string_dict import StringDict


class CommonStatus(str, Enum):
    """Response status."""

    PROCESSING = "Processing"
    FAILED = "Failed"
    PROCESSED = "Processed"


class CommonResponse:
    """Base class for V1 & V2 responses."""

    _raw_http: StringDict
    """Raw request sent by the server, as a dict."""

    def __init__(self, raw_response: StringDict) -> None:
        logger.debug("Handling API response")
        self._raw_http = raw_response

    @property
    def raw_http(self) -> str:
        """Displays the result of the raw response as json string."""
        return json.dumps(self._raw_http, indent=2)
