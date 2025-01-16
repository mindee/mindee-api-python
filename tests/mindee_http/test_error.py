import json
from pathlib import Path

import pytest

from mindee import Client, product
from mindee.error.mindee_http_error import (
    MindeeHTTPClientError,
    MindeeHTTPServerError,
    handle_error,
)
from mindee.input.sources.path_input import PathInput
from tests.test_inputs import FILE_TYPES_DIR
from tests.utils import clear_envvars, dummy_envvars

ERROR_DATA_DIR = Path("./tests/data/errors")


@pytest.fixture
def empty_client(monkeypatch) -> Client:
    clear_envvars(monkeypatch)
    return Client()


@pytest.fixture
def dummy_client(monkeypatch) -> Client:
    dummy_envvars(monkeypatch)
    return Client("dummy")


@pytest.fixture
def dummy_file(monkeypatch) -> PathInput:
    clear_envvars(monkeypatch)
    c = Client(api_key="dummy-client")
    return c.source_from_path(FILE_TYPES_DIR / "pdf" / "blank.pdf")


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
    error_ref = open(ERROR_DATA_DIR / "error_400_no_details.json")
    error_obj = json.load(error_ref)
    error_obj["status_code"] = 400
    error_400 = handle_error("dummy-url", error_obj)
    with pytest.raises(MindeeHTTPClientError):
        raise error_400
    assert error_400.status_code == 400
    assert error_400.api_code == "SomeCode"
    assert error_400.api_message == "Some scary message here"
    assert error_400.api_details is None


def test_http_401_error():
    error_ref = open(ERROR_DATA_DIR / "error_401_invalid_token.json")
    error_obj = json.load(error_ref)
    error_obj["status_code"] = 401
    error_401 = handle_error("dummy-url", error_obj)
    with pytest.raises(MindeeHTTPClientError):
        raise error_401
    assert error_401.status_code == 401
    assert error_401.api_code == "Unauthorized"
    assert error_401.api_message == "Authorization required"
    assert error_401.api_details == "Invalid token provided"


def test_http_429_error():
    error_ref = open(ERROR_DATA_DIR / "error_429_too_many_requests.json")
    error_obj = json.load(error_ref)
    error_obj["status_code"] = 429
    error_429 = handle_error("dummy-url", error_obj)
    with pytest.raises(MindeeHTTPClientError):
        raise error_429
    assert error_429.status_code == 429
    assert error_429.api_code == "TooManyRequests"
    assert error_429.api_message == "Too many requests"
    assert error_429.api_details == "Too Many Requests."


def test_http_500_error():
    error_ref = open(ERROR_DATA_DIR / "error_500_inference_fail.json")
    error_obj = json.load(error_ref)
    error_obj["status_code"] = 500
    error_500 = handle_error("dummy-url", error_obj)
    with pytest.raises(MindeeHTTPServerError):
        raise error_500
    assert error_500.status_code == 500
    assert error_500.api_code == "failure"
    assert error_500.api_message == "Inference failed"
    assert error_500.api_details == "Can not run prediction: "


def test_http_500_html_error():
    error_ref_contents = open(ERROR_DATA_DIR / "error_50x.html").read()
    error_500 = handle_error("dummy-url", error_ref_contents)
    with pytest.raises(MindeeHTTPServerError):
        raise error_500
    assert error_500.status_code == 500
    assert error_500.api_code == "UnknownError"
    assert error_500.api_message == "Server sent back an unexpected reply."
    assert error_500.api_details == error_ref_contents
