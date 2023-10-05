from abc import ABC
from typing import Generic, Optional

from mindee.logger import logger
from mindee.parsing.common.api_request import ApiRequest
from mindee.parsing.common.document import Document
from mindee.parsing.common.inference import TypeInference
from mindee.parsing.common.string_dict import StringDict


class ApiResponse(ABC, Generic[TypeInference]):
    """
    Base class for responses sent by the server.

    Serves as a base class for responses to both synchronous and asynchronous calls.
    """
    
    document: Optional[Document]
    """The document object, properly parsed after being retrieved from the server."""

    raw_http: StringDict
    """Raw request sent by the server, as string."""

    def __init__(self, prediction_type, raw_response: StringDict) -> None:
        logger.debug("Handling API response")
        self.api_request = ApiRequest(raw_response["api_request"])
        self.raw_http = raw_response
        if "document" in raw_response and raw_response["document"]:
            self.document = Document(prediction_type, raw_response["document"])
