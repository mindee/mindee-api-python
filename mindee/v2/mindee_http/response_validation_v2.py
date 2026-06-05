import json

import requests

from mindee.mindee_http import is_valid_sync_response


def is_valid_post_response(response: requests.Response) -> bool:
    """
    Checks if the POST response is valid and of the expected format.

    :param response: HTTP response object.
    :return: True if the response is valid.
    """
    if not is_valid_sync_response(response):
        return False
    response_json = json.loads(response.content)
    if "job" not in response_json:
        return False
    return "job" in response_json and not response_json["job"].get("error")


def is_valid_get_response(response: requests.Response) -> bool:
    """
    Checks if the GET response is valid and of the expected format.

    :param response: HTTP response object.
    :return: True if the response is valid.
    """
    if not is_valid_sync_response(response):
        return False
    response_json = json.loads(response.content)
    return (
        "inference" in response_json
        or "job" in response_json
        or "models" in response_json
    )
