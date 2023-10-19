from typing import Union

from mindee.error.mindee_error import MindeeError
from mindee.error.mindee_http_error import MindeeHTTPError
from mindee.parsing.common.string_dict import StringDict


class MindeeHTTPClientError(MindeeHTTPError):
    """API Client HTTP exception."""


class MindeeHTTPServerError(MindeeHTTPError):
    """API Server HTTP exception."""


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


def handle_error(url: str, response: StringDict, code: int) -> MindeeHTTPError:
    """
    Creates an appropriate HTTP error exception, based on retrieved HTTP error code.

    :param url: url of the product
    :param response: StringDict
    """
    error_obj = create_error_obj(response)
    if 400 <= code <= 499:
        return MindeeHTTPClientError(error_obj, url, code)
    if 500 <= code <= 599:
        return MindeeHTTPServerError(error_obj, url, code)
    return MindeeHTTPError(error_obj, url, code)
