from mindee.parsing.common.string_dict import StringDict


class ErrorResponse:
    """Error response info."""

    detail: str
    """Detail relevant to the error."""
    status: int
    """Http error code."""

    def __init__(self, raw_response: StringDict):
        self.detail = raw_response["detail"]
        self.status = raw_response["status"]

    def __str__(self):
        return f"HTTP Status: {self.status} - {self.detail}"
