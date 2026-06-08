import json

import pytest

from mindee.error.mindee_http_error import (
    MindeeHTTPClientError,
    MindeeHTTPServerError,
    handle_error,
)
from mindee.input.path_input import PathInput
from mindee.v1 import product
from mindee.v1.client import Client
from tests.utils import FILE_TYPES_DIR, V1_ERROR_DATA_DIR, clear_envvars, dummy_envvars


@pytest.fixture
def empty_client(monkeypatch) -> Client:
    clear_envvars(monkeypatch)
    return Client()


@pytest.fixture
def dummy_client(monkeypatch) -> Client:
    dummy_envvars(monkeypatch)
    return Client("dummy")


@pytest.fixture
def dummy_file() -> PathInput:
    return PathInput(FILE_TYPES_DIR / "pdf" / "blank.pdf")


def test_http_client_error(dummy_client: Client, dummy_file: PathInput):
    with pytest.raises(MindeeHTTPClientError):
        dummy_client.parse(product.InvoiceV4, dummy_file)


def test_http_enqueue_client_error(dummy_client: Client, dummy_file: PathInput):
    with pytest.raises(MindeeHTTPClientError):
        dummy_client.enqueue(product.InvoiceV4, dummy_file)


def test_http_parse_client_error(dummy_client: Client, dummy_file: PathInput):
    with pytest.raises(MindeeHTTPClientError):
        dummy_client.parse_queued(product.InvoiceV4, "dummy-queue-id")


def test_http_enqueue_and_parse_client_error(
    dummy_client: Client, dummy_file: PathInput
):
    with pytest.raises(MindeeHTTPClientError):
        dummy_client.enqueue_and_parse(product.InvoiceV4, dummy_file)


def test_http_400_error():
    with open(V1_ERROR_DATA_DIR / "error_400_no_details.json") as e:
        error_obj = json.load(e)
    error_obj["status_code"] = 400
    error_400 = handle_error("dummy-url", error_obj)
    with pytest.raises(MindeeHTTPClientError):
        raise error_400
    assert error_400.status_code == 400
    assert error_400.api_code == "SomeCode"
    assert error_400.api_message == "Some scary message here"
    assert error_400.api_details is None


def test_http_401_error():
    with open(V1_ERROR_DATA_DIR / "error_401_invalid_token.json") as e:
        error_obj = json.load(e)
    error_obj["status_code"] = 401
    error_401 = handle_error("dummy-url", error_obj)
    with pytest.raises(MindeeHTTPClientError):
        raise error_401
    assert error_401.status_code == 401
    assert error_401.api_code == "Unauthorized"
    assert error_401.api_message == "Authorization required"
    assert error_401.api_details == "Invalid token provided"


def test_http_429_error():
    with open(V1_ERROR_DATA_DIR / "error_429_too_many_requests.json") as e:
        error_obj = json.load(e)
    error_obj["status_code"] = 429
    error_429 = handle_error("dummy-url", error_obj)
    with pytest.raises(MindeeHTTPClientError):
        raise error_429
    assert error_429.status_code == 429
    assert error_429.api_code == "TooManyRequests"
    assert error_429.api_message == "Too many requests"
    assert error_429.api_details == "Too Many Requests."


def test_http_500_error():
    with open(V1_ERROR_DATA_DIR / "error_500_inference_fail.json") as e:
        error_obj = json.load(e)
    error_obj["status_code"] = 500
    error_500 = handle_error("dummy-url", error_obj)
    with pytest.raises(MindeeHTTPServerError):
        raise error_500
    assert error_500.status_code == 500
    assert error_500.api_code == "failure"
    assert error_500.api_message == "Inference failed"
    assert error_500.api_details == "Can not run prediction: "


def test_http_500_html_error():
    with open(V1_ERROR_DATA_DIR / "error_50x.html") as e:
        error_ref_contents = e.read()
    error_500 = handle_error("dummy-url", error_ref_contents)
    with pytest.raises(MindeeHTTPServerError):
        raise error_500
    assert error_500.status_code == 500
    assert error_500.api_code == "UnknownError"
    assert error_500.api_message == "Server sent back an unexpected reply."
    assert error_500.api_details == error_ref_contents
