from abc import ABC
from typing import Any, Dict

from mindee.parsing.common.api_request import ApiRequest


StringDict = Dict[str, Any]

class ApiResponse(ABC):
    
    raw_http: StringDict
    """Raw request sent by the server, as string."""
    def __init__(self, server_response: StringDict):
        self.api_request = ApiRequest(server_response["api_request"])
        self.raw_http = server_response
