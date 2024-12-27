from typing import Optional, Union

from mindee.error.mindee_error import MindeeError
from mindee.parsing.common.string_dict import StringDict


class MindeeHTTPError(RuntimeError):
    """An exception relating to HTTP calls."""

    status_code: int
    api_code: Optional[str]
    api_details: Optional[str]
    api_message: Optional[str]

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


def create_error_obj(response: Union[StringDict, str]) -> StringDict:
    """
    Creates an error object based on a requests' payload.

    :param response: response as sent by the server, as a dict.
        In _very_ rare instances, this can be an html string.
    """
    if not isinstance(response, str):
        if "api_request" in response and "error" in response["api_request"]:
            return response["api_request"]["error"]
        raise MindeeError(f"Could not build specific HTTP exception from '{response}'")
    error_dict = {}
    if "Maximum pdf pages" in response:
        error_dict = {
            "code": "TooManyPages",
            "message": "Maximum amound of pdf pages reached.",
            "details": response,
        }
    elif "Max file size is" in response:
        error_dict = {
            "code": "FileTooLarge",
            "message": "Maximum file size reached.",
            "details": response,
        }
    elif "Invalid file type" in response:
        error_dict = {
            "code": "InvalidFiletype",
            "message": "Invalid file type.",
            "details": response,
        }
    elif "Gateway timeout" in response:
        error_dict = {
            "code": "RequestTimeout",
            "message": "Request timed out.",
            "details": response,
        }
    elif "Too Many Requests" in response:
        error_dict = {
            "code": "TooManyRequests",
            "message": "Too Many Requests.",
            "details": response,
        }
    else:
        error_dict = {
            "code": "UnknownError",
            "message": "Server sent back an unexpected reply.",
            "details": response,
        }
    return error_dict


class MindeeHTTPClientError(MindeeHTTPError):
    """API Client HTTP exception."""


class MindeeHTTPServerError(MindeeHTTPError):
    """API Server HTTP exception."""


def handle_error(url: str, response: StringDict) -> MindeeHTTPError:
    """
    Creates an appropriate HTTP error exception, based on retrieved HTTP error code.

    :param url: url of the product
    :param response: StringDict
    """
    error_obj = create_error_obj(response)
    if not isinstance(response, str) and (  # type: ignore
        "status_code" in response
        and (
            isinstance(response["status_code"], int)
            or response["status_code"].isdigit()
        )
    ):
        code = int(response["status_code"])
    else:
        code = 500
    if 400 <= code <= 499:
        return MindeeHTTPClientError(error_obj, url, code)
    if 500 <= code <= 599:
        return MindeeHTTPServerError(error_obj, url, code)
    return MindeeHTTPError(error_obj, url, code)
