import os
from datetime import datetime
from pathlib import Path
from time import sleep

import httpx
import pytest

from mindee import ExtractionParameters
from mindee.input.path_input import PathInput
from mindee.input.url_input_source import URLInputSource
from mindee.v2.client import Client
from mindee.v2.error.mindee_http_error_v2 import (
    MindeeHTTPErrorV2,
)
from mindee.v2.parsing import InferenceActiveOptions
from mindee.v2.parsing.job.job import Job
from mindee.v2.product.extraction.extraction_response import ExtractionResponse
from mindee.v2.product.split.params.split_parameters import SplitParameters
from mindee.v2.product.split.split_response import SplitResponse
from tests.utils import FILE_TYPES_PATH, V2_PRODUCT_PATH


@pytest.fixture(scope="session")
def v2_client() -> Client:
    return Client()


def _basic_assert_success(
    response: ExtractionResponse, page_count: int, model_id: str
) -> None:
    assert response is not None
    assert response.inference is not None

    assert response.inference.file is not None
    assert response.inference.file.page_count == page_count

    assert response.inference.model is not None
    assert response.inference.model.id == model_id

    assert response.inference.result is not None
    assert response.inference.active_options is not None


@pytest.mark.integration
@pytest.mark.v2
def test_parse_file_empty_multiple_pages_must_succeed(
    v2_client: Client, findoc_model_id: str
) -> None:
    """
    Upload a 2-page almost blank PDF and make sure the returned inference contains the
    file & model metadata.
    """
    input_path: Path = FILE_TYPES_PATH / "pdf" / "multipage_cut-2.pdf"

    input_source = PathInput(input_path)
    params = ExtractionParameters(
        model_id=findoc_model_id,
        rag=False,
        raw_text=True,
        polygon=False,
        confidence=False,
        alias="py_integration_empty_multiple",
    )

    response: ExtractionResponse = v2_client.enqueue_and_get_result(
        ExtractionResponse, input_source, params
    )
    _basic_assert_success(response=response, page_count=2, model_id=findoc_model_id)

    assert response.inference.file.name == "multipage_cut-2.pdf"

    assert response.inference.model is not None
    assert response.inference.model.id == findoc_model_id

    assert isinstance(response.inference.active_options, InferenceActiveOptions)
    assert response.inference.active_options is not None
    assert response.inference.active_options.rag is False
    assert response.inference.active_options.raw_text is True
    assert response.inference.active_options.polygon is False
    assert response.inference.active_options.confidence is False
    assert response.inference.active_options.text_context is False

    assert response.inference.result.raw_text is not None
    assert len(response.inference.result.raw_text.pages) == 2


@pytest.mark.integration
@pytest.mark.v2
def test_parse_file_empty_single_page_options_must_succeed(
    v2_client: Client, findoc_model_id: str
) -> None:
    """
    Upload a blank PDF and make sure the options are set correctly.
    """
    input_path: Path = FILE_TYPES_PATH / "pdf" / "blank_1.pdf"

    input_source = PathInput(input_path)
    params = ExtractionParameters(
        model_id=findoc_model_id,
        rag=True,
        raw_text=True,
        polygon=True,
        confidence=True,
        alias="py_integration_empty_page_options",
    )
    response: ExtractionResponse = v2_client.enqueue_and_get_result(
        ExtractionResponse, input_source, params
    )
    _basic_assert_success(response=response, page_count=1, model_id=findoc_model_id)

    assert response.inference.file.name == "blank_1.pdf"

    assert isinstance(response.inference.active_options, InferenceActiveOptions)
    assert response.inference.active_options is not None
    assert response.inference.active_options.rag is True
    assert response.inference.active_options.raw_text is True
    assert response.inference.active_options.polygon is True
    assert response.inference.active_options.confidence is True
    assert response.inference.active_options.text_context is False


@pytest.mark.integration
@pytest.mark.v2
def test_parse_file_filled_single_page_must_succeed(
    v2_client: Client, findoc_model_id: str
) -> None:
    """
    Upload a filled single-page JPEG and verify that common fields are present.
    """
    input_path: Path = (
        V2_PRODUCT_PATH / "extraction" / "financial_document" / "default_sample.jpg"
    )

    input_source = PathInput(input_path)
    params = ExtractionParameters(
        model_id=findoc_model_id,
        webhook_ids=[],
        rag=None,
        raw_text=None,
        polygon=None,
        confidence=None,
        alias="py_integration_filled_single",
        text_context="this is an invoice.",
    )

    response: ExtractionResponse = v2_client.enqueue_and_get_result(
        ExtractionResponse, input_source, params
    )
    _basic_assert_success(response=response, page_count=1, model_id=findoc_model_id)

    assert response.inference.file.name == "default_sample.jpg"

    assert response.inference.model is not None
    assert response.inference.model.id == findoc_model_id

    assert isinstance(response.inference.active_options, InferenceActiveOptions)
    assert response.inference.active_options is not None
    assert response.inference.active_options.rag is False
    assert response.inference.active_options.raw_text is False
    assert response.inference.active_options.polygon is False
    assert response.inference.active_options.confidence is False
    assert response.inference.active_options.text_context is True

    assert response.inference.result.raw_text is None

    supplier_name = response.inference.result.fields["supplier_name"]
    assert supplier_name is not None
    assert supplier_name.value == "John Smith"
    assert supplier_name.confidence is None
    assert len(supplier_name.locations) == 0


def _enqueue_and_poll_job(v2_client: Client, input_source, params) -> Job:
    """Enqueue a document and poll until the job reaches a final status."""
    job = v2_client.enqueue(input_source, params).job
    for _ in range(60):
        sleep(2)
        job = v2_client.get_job(job.id).job
        if job.status in {"Processed", "Failed"}:
            break
    return job


def _assert_webhook_job_success(job: Job, webhook_ids: list) -> None:
    assert job.status == "Processed"
    assert isinstance(job.completed_at, datetime)
    assert job.error is None
    assert len(job.webhooks) == len(webhook_ids)
    assert all(webhook.status in {"Completed", "Failed"} for webhook in job.webhooks)
    assert {webhook.id for webhook in job.webhooks} == set(webhook_ids)


@pytest.mark.integration
@pytest.mark.v2
def test_extraction_with_two_webhooks_must_complete_and_succeed(
    v2_client: Client, findoc_model_id: str
) -> None:
    webhook_ids = [
        "9a0d88be-6913-484d-a019-9d2e16e2d3b9",
        "32286ed9-fe40-4f42-bdc5-2f8496c5641a",
    ]

    input_source = PathInput(
        V2_PRODUCT_PATH / "extraction" / "financial_document" / "default_sample.jpg"
    )
    params = ExtractionParameters(model_id=findoc_model_id, webhook_ids=webhook_ids)

    job = _enqueue_and_poll_job(v2_client, input_source, params)
    _assert_webhook_job_success(job, webhook_ids)

    response = v2_client.get_result_from_url(ExtractionResponse, job.result_url)
    assert response.inference is not None
    assert response.inference.result is not None
    assert response.inference.result.fields["supplier_name"].value == "John Smith"


@pytest.mark.integration
@pytest.mark.v2
def test_split_with_two_webhooks_must_complete_and_succeed(
    v2_client: Client, split_model_id: str
) -> None:
    webhook_ids = [
        "b8fdfea3-24b6-438a-a6ca-7cd8c87a8875",
        "d5bf36a9-1301-42c7-95be-03dc20d8f10e",
    ]

    input_source = PathInput(V2_PRODUCT_PATH / "split" / "default_sample.pdf")
    params = SplitParameters(model_id=split_model_id, webhook_ids=webhook_ids)

    job = _enqueue_and_poll_job(v2_client, input_source, params)
    _assert_webhook_job_success(job, webhook_ids)

    response = v2_client.get_result_from_url(SplitResponse, job.result_url)
    assert response.inference is not None
    assert response.inference.result is not None
    assert len(response.inference.result.splits) == 2


@pytest.mark.integration
@pytest.mark.v2
def test_invalid_uuid_must_throw_error(v2_client: Client) -> None:
    """
    Using an invalid model identifier must trigger a 422 HTTP error.
    """
    input_path: Path = FILE_TYPES_PATH / "pdf" / "blank_1.pdf"

    input_source = PathInput(input_path)
    params = ExtractionParameters(
        model_id="INVALID MODEL ID", text_context="ignore this message"
    )

    with pytest.raises(MindeeHTTPErrorV2) as e:
        v2_client.enqueue(input_source, params)

    exc: MindeeHTTPErrorV2 = e.value
    assert exc.status == 422
    assert exc.title is not None
    assert exc.code.startswith("422-")
    assert isinstance(exc.errors, list)


@pytest.mark.integration
@pytest.mark.v2
def test_unknown_model_must_throw_error(v2_client: Client) -> None:
    """
    Using an unknown model identifier must trigger a 404 HTTP error.
    """
    input_path: Path = FILE_TYPES_PATH / "pdf" / "blank_1.pdf"

    input_source = PathInput(input_path)
    params = ExtractionParameters(model_id="fc405e37-4ba4-4d03-aeba-533a8d1f0f21")

    with pytest.raises(MindeeHTTPErrorV2) as e:
        v2_client.enqueue(input_source, params)

    exc: MindeeHTTPErrorV2 = e.value
    assert exc.status == 404
    assert exc.title is not None
    assert exc.code.startswith("404-")
    assert isinstance(exc.errors, list)


@pytest.mark.integration
@pytest.mark.v2
def test_unknown_webhook_ids_must_throw_error(
    v2_client: Client, findoc_model_id: str
) -> None:
    """
    Using an unknown webhook identifier must trigger an error.
    """
    input_path: Path = FILE_TYPES_PATH / "pdf" / "blank_1.pdf"

    input_source = PathInput(input_path)
    params = ExtractionParameters(
        model_id=findoc_model_id,
        webhook_ids=[
            "fc405e37-4ba4-4d03-aeba-533a8d1f0f21",
            "fc405e37-4ba4-4d03-aeba-533a8d1f0f21",
        ],
        rag=None,
        raw_text=None,
        polygon=None,
        confidence=None,
    )

    with pytest.raises(MindeeHTTPErrorV2) as e:
        v2_client.enqueue(input_source, params)

    exc: MindeeHTTPErrorV2 = e.value
    assert exc.status == 422
    assert exc.title is not None
    assert exc.code.startswith("422-")
    assert isinstance(exc.errors, list)
    assert "no matching webhooks" in exc.detail.lower()


@pytest.mark.integration
@pytest.mark.v2
def test_blank_url_input_source_must_succeed(
    v2_client: Client,
    findoc_model_id: str,
) -> None:
    """
    Load a blank PDF from an HTTPS URL and make sure the inference call completes without raising any errors.
    """
    url = os.getenv("MINDEE_V2_SE_TESTS_BLANK_PDF_URL")

    input_source = URLInputSource(url)
    params = ExtractionParameters(
        model_id=findoc_model_id,
        rag=False,
        raw_text=False,
        polygon=False,
        confidence=False,
        webhook_ids=[],
        alias="py_integration_url_source",
    )
    response: ExtractionResponse = v2_client.enqueue_and_get_result(
        ExtractionResponse, input_source, params
    )
    _basic_assert_success(response=response, page_count=1, model_id=findoc_model_id)


@pytest.mark.integration
@pytest.mark.v2
def test_data_schema_must_succeed(
    v2_client: Client,
    findoc_model_id: str,
) -> None:
    """
    Load a blank PDF from an HTTPS URL and make sure the inference call completes without raising any errors.
    """
    input_path: Path = FILE_TYPES_PATH / "pdf" / "blank_1.pdf"
    data_schema_replace_path = (
        V2_PRODUCT_PATH / "extraction" / "data_schema_replace_param.json"
    )

    input_source = PathInput(input_path)
    params = ExtractionParameters(
        model_id=findoc_model_id,
        rag=False,
        raw_text=False,
        polygon=False,
        confidence=False,
        webhook_ids=[],
        data_schema=data_schema_replace_path.read_text(),
        alias="py_integration_data_schema_replace",
    )
    response: ExtractionResponse = v2_client.enqueue_and_get_result(
        ExtractionResponse, input_source, params
    )
    _basic_assert_success(response=response, page_count=1, model_id=findoc_model_id)
    assert response.inference.active_options.data_schema.replace is True
    assert response.inference.result.fields["test_replace"] is not None
    assert response.inference.result.fields["test_replace"].value == "a test value"


@pytest.mark.integration
@pytest.mark.v2
def test_custom_httpx_client_event_hook(
    findoc_model_id: str,
) -> None:
    request_urls = []

    def log_request(request: httpx.Request):
        request_urls.append(str(request.url))

    httpx_client = httpx.Client(event_hooks={"request": [log_request]})
    client = Client(http_client=httpx_client)

    input_path = FILE_TYPES_PATH / "pdf" / "blank_1.pdf"
    input_source = PathInput(input_path)

    params = ExtractionParameters(
        model_id=findoc_model_id,
        rag=False,
        raw_text=False,
        polygon=False,
        confidence=False,
        webhook_ids=[],
        alias="py_integration_custom_httpx_client",
    )

    client.enqueue(input_source, params)

    assert len(request_urls) > 0
    assert any("enqueue" in url for url in request_urls)


@pytest.mark.v2
@pytest.mark.integration
def test_http2_client(findoc_model_id) -> None:
    httpx_client = httpx.Client(http2=True)
    with Client(http_client=httpx_client) as client:
        input_source = PathInput(
            V2_PRODUCT_PATH / "extraction" / "financial_document" / "default_sample.jpg"
        )
        params = ExtractionParameters(model_id=findoc_model_id)
        response = client.enqueue_and_get_result(
            ExtractionResponse, input_source, params
        )
        _basic_assert_success(response, page_count=1, model_id=findoc_model_id)
