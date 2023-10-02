import json

import pytest

from mindee import Client
from mindee.http.mindee_api import OTS_OWNER
from mindee.input.sources import PathInput
from mindee.parsing.common.async_predict_response import AsyncPredictResponse
from mindee.parsing.common.document import Document
from mindee.product.invoice_splitter import InvoiceSplitterV1

ASYNC_DIR = "./tests/data/async"

FILE_PATH_POST_SUCCESS = f"{ ASYNC_DIR }/post_success.json"
FILE_PATH_POST_FAIL = f"{ ASYNC_DIR }/post_fail_forbidden.json"
FILE_PATH_GET_PROCESSING = f"{ ASYNC_DIR }/get_processing.json"
FILE_PATH_GET_COMPLETED = f"{ ASYNC_DIR }/get_completed.json"


@pytest.fixture
def dummy_file_input():
    file_input = PathInput("./tests/data/products/invoice_splitter/default_sample.pdf")
    return file_input


@pytest.fixture
def dummy_config():
    client = Client(api_key="dummy").add_endpoint(
        endpoint_name="dummy",
        account_name="dummy",
    )
    return client._doc_configs


def test_constructor(dummy_file_input):
    with pytest.raises(KeyError):
        Document(
            dummy_file_input,
            document_type="invoice_splitter",
            api_prediction={},
            page_id=0,
        )


def test_async_response_post_success(dummy_file_input, dummy_config):
    response = json.load(open(FILE_PATH_POST_SUCCESS))
    parsed_response = AsyncPredictResponse[InvoiceSplitterV1](
        doc_config=dummy_config[(OTS_OWNER, InvoiceSplitterV1.__name__)],
        http_response=response,
        input_source=dummy_file_input,
        response_ok=True,
    )
    assert parsed_response.job is not None
    assert (
        parsed_response.job.issued_at.isoformat() == "2023-02-16T12:33:49.602947+00:00"
    )
    assert parsed_response.job.available_at is None
    assert parsed_response.job.status == "waiting"
    assert parsed_response.job.id == "76c90710-3a1b-4b91-8a39-31a6543e347c"
    assert not parsed_response.api_request.error


def test_async_response_post_fail(dummy_file_input, dummy_config):
    response = json.load(open(FILE_PATH_POST_FAIL))
    parsed_response = AsyncPredictResponse[InvoiceSplitterV1](
        doc_config=dummy_config[(OTS_OWNER, InvoiceSplitterV1.__name__)],
        http_response=response,
        input_source=dummy_file_input,
        response_ok=True,
    )
    assert parsed_response.job is not None
    assert parsed_response.job.issued_at.isoformat() == "2023-01-01T00:00:00+00:00"
    assert parsed_response.job.available_at is None
    assert parsed_response.job.status is None
    assert parsed_response.job.id is None
    assert parsed_response.api_request.error
    assert parsed_response.api_request.error["code"] == "Forbidden"


def test_async_get_processing(dummy_file_input, dummy_config):
    response = json.load(open(FILE_PATH_GET_PROCESSING))
    parsed_response = AsyncPredictResponse[InvoiceSplitterV1](
        doc_config=dummy_config[(OTS_OWNER, InvoiceSplitterV1.__name__)],
        http_response=response,
        input_source=dummy_file_input,
        response_ok=True,
    )
    assert parsed_response.job is not None
    assert parsed_response.job.issued_at.isoformat() == "2023-03-16T12:33:49.602947"
    assert parsed_response.job.available_at is None
    assert parsed_response.job.status == "processing"
    assert parsed_response.job.id == "76c90710-3a1b-4b91-8a39-31a6543e347c"
    assert not parsed_response.api_request.error


def test_async_response_get_completed(dummy_file_input, dummy_config):
    response = json.load(open(FILE_PATH_GET_COMPLETED))
    parsed_response = AsyncPredictResponse[InvoiceSplitterV1](
        doc_config=dummy_config[(OTS_OWNER, InvoiceSplitterV1.__name__)],
        http_response=response,
        input_source=dummy_file_input,
        response_ok=True,
    )
    assert parsed_response.job is not None
    assert parsed_response.job.issued_at.isoformat() == "2023-03-21T13:52:56.326107"
    assert parsed_response.job.available_at.isoformat() == "2023-03-21T13:53:00.990339"
    assert parsed_response.job.status == "completed"
    assert parsed_response.api_request.error == {}
