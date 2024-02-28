import requests
import json


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
    if "job" not in response_json:
        return False
    if (
            "job" in response_json
            and "error" in response_json["job"]
            and response_json["job"]["error"]
    ):
        return False
    return True
