import json
from pathlib import Path

import pytest
import requests

from mindee.client import Client
from mindee.input.sources.path_input import PathInput
from mindee.mindee_http.response_validation import is_valid_async_response
from mindee.parsing.common.api_request import RequestStatus
from mindee.parsing.common.async_predict_response import AsyncPredictResponse
from mindee.product.invoice_splitter.invoice_splitter_v1 import InvoiceSplitterV1

ASYNC_DIR = Path("./tests/data/async")

FILE_PATH_POST_SUCCESS = ASYNC_DIR / "post_success.json"
FILE_PATH_POST_FAIL = ASYNC_DIR / "post_fail_forbidden.json"
FILE_PATH_GET_PROCESSING = ASYNC_DIR / "get_processing.json"
FILE_PATH_GET_COMPLETED = ASYNC_DIR / "get_completed.json"
FILE_PATH_GET_FAILED_JOB = ASYNC_DIR / "get_failed_job_error.json"


class FakeResponse(requests.Response):
    def __init__(self, json_data, _status_code=200):
        super().__init__()
        self._json_data = json_data
        self.status_code = _status_code
        self._ok = True

    def set_ok_status(self, ok_status):
        self._ok = ok_status

    @property
    def ok(self):
        return self._ok

    @property
    def content(self) -> str:
        return json.dumps(self._json_data)


@pytest.fixture
def dummy_file_input() -> PathInput:
    file_input = PathInput("./tests/data/products/invoice_splitter/default_sample.pdf")
    return file_input


@pytest.fixture
def dummy_client() -> Client:
    return Client(api_key="dummy")


def test_async_response_post_success():
    response = json.load(open(FILE_PATH_POST_SUCCESS))
    parsed_response = AsyncPredictResponse(InvoiceSplitterV1, response)
    fake_response = FakeResponse(response)
    fake_response.set_ok_status(True)
    assert is_valid_async_response(fake_response) is True
    assert parsed_response.job is not None
    assert (
        parsed_response.job.issued_at.isoformat() == "2023-02-16T12:33:49.602947+00:00"
    )
    assert parsed_response.job.available_at is None
    assert parsed_response.job.status == "waiting"
    assert parsed_response.job.id == "76c90710-3a1b-4b91-8a39-31a6543e347c"
    assert not parsed_response.api_request.error


def test_async_response_post_fail():
    response = json.load(open(FILE_PATH_POST_FAIL))
    fake_response = FakeResponse(response)
    fake_response.set_ok_status(False)
    assert is_valid_async_response(fake_response) is False


def test_async_get_processing():
    response = json.load(open(FILE_PATH_GET_PROCESSING))
    parsed_response = AsyncPredictResponse(InvoiceSplitterV1, response)
    fake_response = FakeResponse(response)
    fake_response.set_ok_status(True)
    assert is_valid_async_response(fake_response) is True
    assert parsed_response.job is not None
    assert parsed_response.job.issued_at.isoformat() == "2023-03-16T12:33:49.602947"
    assert parsed_response.job.available_at is None
    assert parsed_response.job.status == "processing"
    assert parsed_response.job.id == "76c90710-3a1b-4b91-8a39-31a6543e347c"
    assert not parsed_response.api_request.error


def test_async_response_get_completed():
    response = json.load(open(FILE_PATH_GET_COMPLETED))
    parsed_response = AsyncPredictResponse(InvoiceSplitterV1, response)
    fake_response = FakeResponse(response)
    fake_response.set_ok_status(True)
    assert is_valid_async_response(fake_response) is True
    assert parsed_response.job is not None
    assert parsed_response.job.issued_at.isoformat() == "2023-03-21T13:52:56.326107"
    assert parsed_response.job.available_at.isoformat() == "2023-03-21T13:53:00.990339"
    assert parsed_response.job.status == "completed"
    assert parsed_response.api_request.error == {}


def test_async_get_failed_job():
    response = json.load(open(FILE_PATH_GET_FAILED_JOB))
    parsed_response = AsyncPredictResponse(InvoiceSplitterV1, response)
    fake_response = FakeResponse(response)
    fake_response.set_ok_status(False)
    assert is_valid_async_response(fake_response) is False
    assert parsed_response.api_request.status == RequestStatus.SUCCESS
    assert parsed_response.api_request.status_code == 200
    assert parsed_response.job.issued_at.isoformat() == "2024-02-20T10:31:06.878599"
    assert parsed_response.job.available_at.isoformat() == "2024-02-20T10:31:06.878599"
    assert parsed_response.job.status == "failed"
    assert parsed_response.job.error["code"] == "ServerError"
