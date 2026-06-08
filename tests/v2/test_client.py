import concurrent.futures
import json
import os
import re
import time

import httpx
import pytest
import respx

from mindee import ExtractionParameters, ExtractionResponse, LocalResponse
from mindee.error.mindee_error import MindeeError
from mindee.input.local_input_source import LocalInputSource
from mindee.input.path_input import PathInput
from mindee.v1.mindee_http.base_settings import USER_AGENT
from mindee.v2.client import Client
from mindee.v2.error.mindee_api_v2_error import MindeeAPIV2Error
from mindee.v2.error.mindee_http_error_v2 import (
    MindeeHTTPErrorV2,
    MindeeHTTPUnknownErrorV2,
)
from mindee.v2.parsing.job.job import Job
from mindee.v2.parsing.job.job_response import JobResponse
from mindee.v2.product.extraction.extraction_inference import ExtractionInference
from tests.utils import FILE_TYPES_DIR, V2_DATA_DIR, V2_PRODUCT_DATA_DIR, dummy_envvars


@pytest.fixture
def env_client(monkeypatch) -> Client:
    dummy_envvars(monkeypatch)
    return Client("dummy")


@pytest.fixture
def custom_base_url_client(monkeypatch) -> Client:
    class _FakePostRespError:
        status_code = 400
        is_error = True

        def json(self):
            return {
                "status": 0,
                "code": "000-000",
                "title": "From Test",
                "detail": "forced failure from test",
            }

    class _FakeOkProcessingJobResp:
        status_code = 200
        is_error = False

        def json(self):
            data_file = V2_DATA_DIR / "job" / "ok_processing.json"
            with data_file.open("r", encoding="utf-8") as fh:
                return json.load(fh)

        @property
        def content(self) -> bytes:
            """
            Raw (bytes) payload, mimicking `requests.Response.content`.
            """
            return json.dumps(self.json()).encode("utf-8")

    class _FakeOkGetInferenceResp:
        status_code = 200
        is_error = False

        def json(self):
            data_file = (
                V2_PRODUCT_DATA_DIR
                / "extraction"
                / "financial_document"
                / "complete.json"
            )
            with data_file.open("r", encoding="utf-8") as fh:
                return json.load(fh)

        @property
        def content(self) -> bytes:
            """
            Raw (bytes) payload, mimicking `requests.Response.content`.
            """
            return json.dumps(self.json()).encode("utf-8")

    monkeypatch.setenv("MINDEE_V2_BASE_URL", "https://dummy-url")

    def _fake_error_post_inference_enqueue(*args, **kwargs):
        return _FakePostRespError()

    def _fake_ok_get_job(*args, **kwargs):
        return _FakeOkProcessingJobResp()

    def _fake_ok_get_inference(*args, **kwargs):
        return _FakeOkGetInferenceResp()

    monkeypatch.setattr(
        "mindee.v2.mindee_http.mindee_api_v2.MindeeAPIV2.req_post_inference_enqueue",
        _fake_error_post_inference_enqueue,
        raising=True,
    )

    monkeypatch.setattr(
        "mindee.v2.mindee_http.mindee_api_v2.MindeeAPIV2.req_get_job",
        _fake_ok_get_job,
        raising=True,
    )

    monkeypatch.setattr(
        "mindee.v2.mindee_http.mindee_api_v2.MindeeAPIV2.req_get_inference",
        _fake_ok_get_inference,
        raising=True,
    )

    return Client("dummy")


@pytest.fixture
def env_no_key(monkeypatch):
    if os.getenv("MINDEE_V2_API_KEY"):
        monkeypatch.delenv("MINDEE_V2_API_KEY")


@pytest.mark.v2
def test_parse_path_without_token(env_no_key):
    with pytest.raises(MindeeAPIV2Error):
        Client()


@pytest.mark.v2
def test_enqueue_path_with_env_token(custom_base_url_client):
    assert custom_base_url_client.mindee_api.base_url == "https://dummy-url"
    assert custom_base_url_client.mindee_api.url_root == "https://dummy-url"
    assert custom_base_url_client.mindee_api.api_key == "dummy"
    assert custom_base_url_client.mindee_api.base_headers["Authorization"] == "dummy"
    assert custom_base_url_client.mindee_api.base_headers["User-Agent"] == USER_AGENT
    input_doc: LocalInputSource = PathInput(f"{FILE_TYPES_DIR}/receipt.jpg")
    with pytest.raises(MindeeHTTPErrorV2):
        custom_base_url_client.enqueue(input_doc, ExtractionParameters("dummy-model"))


@pytest.mark.v2
def test_enqueue_and_parse_path_with_env_token(custom_base_url_client):
    input_doc: LocalInputSource = PathInput(f"{FILE_TYPES_DIR}/receipt.jpg")
    with pytest.raises(MindeeHTTPErrorV2):
        custom_base_url_client.enqueue_and_get_result(
            ExtractionResponse,
            input_doc,
            ExtractionParameters(
                "dummy-model",
                text_context="ignore this message",
                data_schema=json.loads(
                    (
                        V2_PRODUCT_DATA_DIR
                        / "extraction"
                        / "data_schema_replace_param.json"
                    ).read_text()
                ),
            ),
        )


def _assert_findoc_inference(response: ExtractionResponse):
    assert isinstance(response, ExtractionResponse)
    assert isinstance(response.inference, ExtractionInference)
    assert response.inference.id
    assert response.inference.model.id
    assert len(response.inference.result.fields) > 1


@pytest.mark.v2
def test_loads_from_prediction():
    input_inference = LocalResponse(
        V2_PRODUCT_DATA_DIR / "extraction" / "financial_document" / "complete.json"
    )
    response = input_inference.deserialize_response(ExtractionResponse)
    _assert_findoc_inference(response)
    with pytest.raises(MindeeError):
        input_inference.deserialize_response(JobResponse)


@pytest.mark.v2
def test_get_inference(custom_base_url_client):
    response = custom_base_url_client.get_result(
        ExtractionResponse, "12345678-1234-1234-1234-123456789ABC"
    )
    _assert_findoc_inference(response)


@pytest.mark.v2
def test_get_inference_by_url(custom_base_url_client):
    response = custom_base_url_client.get_result(
        ExtractionResponse,
        "https://api-v2.mindee.net/v2/inference/12345678-1234-1234-1234-123456789ABC",
    )
    _assert_findoc_inference(response)


@pytest.mark.v2
def test_error_handling(custom_base_url_client):
    with pytest.raises(MindeeHTTPErrorV2) as e:
        custom_base_url_client.enqueue(
            PathInput(
                V2_PRODUCT_DATA_DIR
                / "extraction"
                / "financial_document"
                / "default_sample.jpg"
            ),
            ExtractionParameters("dummy-model"),
        )
    assert e.value.status == 0
    assert e.value.detail == "forced failure from test"


@pytest.mark.v2
def test_error_handling_non_json_response(env_client, monkeypatch):
    class _FakeHtmlRespError:
        status_code = 502
        is_error = True
        text = "<html><head><title>502 Bad Gateway</title></head></html>"

        def json(self):
            raise httpx.DecodingError("Expecting value")

    def _fake_error_post_inference_enqueue(*args, **kwargs):
        return _FakeHtmlRespError()

    monkeypatch.setattr(
        "mindee.v2.mindee_http.mindee_api_v2.MindeeAPIV2.req_post_inference_enqueue",
        _fake_error_post_inference_enqueue,
        raising=True,
    )

    with pytest.raises(MindeeHTTPUnknownErrorV2) as e:
        env_client.enqueue(
            PathInput(
                V2_PRODUCT_DATA_DIR
                / "extraction"
                / "financial_document"
                / "default_sample.jpg"
            ),
            ExtractionParameters("dummy-model"),
        )
    assert e.value.status == -1
    assert "HTTP 502 response is not valid JSON" in e.value.detail


@pytest.mark.v2
def test_queue_get(custom_base_url_client):
    response = custom_base_url_client.get_job("12345678-1234-1234-1234-123456789ABC")
    assert isinstance(response, JobResponse)
    assert isinstance(response.job, Job)
    assert response.job.id == "12345678-1234-1234-1234-123456789ABC"
    assert response.job.model_id == "87654321-4321-4321-4321-CBA987654321"
    assert response.job.filename == "default_sample.jpg"
    assert response.job.alias == "dummy-alias.jpg"
    assert str(response.job.created_at) == "2025-07-03 14:27:58.974451"
    assert response.job.status == "Processing"
    assert (
        response.job.polling_url
        == "https://api-v2.mindee.net/v2/jobs/12345678-1234-1234-1234-123456789ABC"
    )
    assert not response.job.result_url
    assert len(response.job.webhooks) == 0
    assert not response.job.error


@pytest.mark.v2
def test_client_closes_httpx_connections() -> None:
    client = Client(api_key="dummy_key")
    client.close()
    with pytest.raises(
        RuntimeError, match=r"Cannot send a request, as the client has been closed\."
    ):
        client.mindee_api.http_client.get("https://google.com")


@pytest.mark.v2
@respx.mock
def test_httpx_multiple_calls_thread_safety() -> None:
    client = Client(api_key="dummy_key")
    input_path = FILE_TYPES_DIR / "pdf" / "blank_1.pdf"

    def delayed_response(request: httpx.Request) -> httpx.Response:
        job_json = json.loads((V2_DATA_DIR / "job" / "ok_processing.json").read_text())
        time.sleep(0.1)
        return httpx.Response(201, json=job_json)

    url_pattern = re.compile(r"https://api-v2\.mindee\.net/v2/.+/enqueue")
    respx.post(url_pattern).mock(side_effect=delayed_response)

    def make_request():
        input_source = PathInput(input_path)
        params = ExtractionParameters(model_id="dummy-model-id")
        return client.enqueue(input_source, params)

    thread_count = 20
    successful_responses = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
        futures = [executor.submit(make_request) for _ in range(thread_count)]

        for future in concurrent.futures.as_completed(futures):
            response = future.result()
            if (
                response.job
                and response.job.id == "12345678-1234-1234-1234-123456789ABC"
            ):
                successful_responses += 1

    assert successful_responses == thread_count
