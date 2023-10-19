from mindee.parsing.common.string_dict import StringDict


class MindeeHTTPError(RuntimeError):
    """An exception relating to HTTP calls."""

    status_code: int
    api_code: str
    api_details: str
    api_message: str

    def __init__(self, http_error: StringDict, url: str, code: int) -> None:
        """
        Base exception for HTTP calls.

        :param http_error: formatted & parsed error
        :param url: url/endpoint the exception was raised on
        :param code: HTTP code for the error
        """
        self.status_code = code
        self.api_code = http_error["code"] if "code" in http_error else None
        self.api_details = http_error["details"] if "details" in http_error else None
        self.api_message = http_error["message"] if "message" in http_error else None
        super().__init__(
            f"{url} {self.status_code} HTTP error: {self.api_details} - {self.api_message}"
        )