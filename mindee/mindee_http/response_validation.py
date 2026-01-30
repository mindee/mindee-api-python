import json

import requests

from mindee.parsing.common.string_dict import StringDict


def is_valid_sync_response(response: requests.Response) -> bool:
    """
    Checks if the synchronous response is valid. Returns True if the response is valid.

    :param response: a requests response object.
    :return: bool
    """
    if not response or not response.ok:
        return False
    response_json = json.loads(response.content)
    # VERY rare edge case where raw html is sent instead of json.
    if not isinstance(response_json, dict):
        return False
    return True


def is_valid_async_response(response: requests.Response) -> bool:
    """
    Checks if the asynchronous response is valid. Also checks if it is a valid synchronous response.

    Returns True if the response is valid.

    :param response: a requests response object.
    :return: bool
    """
    if not is_valid_sync_response(response):
        return False
    response_json = json.loads(response.content)
    # Checks invalid status codes within the bounds of ok responses.
    if response.status_code and (
        response.status_code < 200 or response.status_code > 302
    ):
        return False
    # Async errors.
    if "job" not in response_json and "execution" not in response_json:
        return False
    if (
        "job" in response_json
        and "error" in response_json["job"]
        and response_json["job"]["error"]
    ):
        return False

    return True


def clean_request_json(response: requests.Response) -> StringDict:
    """
    Checks and correct the response error format depending on the two possible kind of returns.

    :param response: Raw request response.
    :return: Returns the job error if the error is due to parsing, returns the http error otherwise.
    """
    response_json = response.json()
    if response.status_code < 200 or response.status_code > 302:
        response_json["status_code"] = response.status_code
        return response_json
    corrected_json = response_json
    if (
        "api_request" in response_json
        and "status_code" in response_json["api_request"]
        and isinstance(response_json["api_request"]["status_code"], (int, str))
        and str(response_json["api_request"]["status_code"]).isdigit()
        and int(response_json["api_request"]["status_code"]) >= 400
    ):
        corrected_json["status_code"] = int(response_json["api_request"]["status_code"])
    if (
        "job" in response_json
        and "error" in response_json["job"]
        and response_json["job"]["error"]
    ):
        corrected_json["error"] = response_json["job"]["error"]
        corrected_json["status_code"] = 500
    return corrected_json
