import json

import pytest

from mindee import ClientV2, InferenceParameters, InferenceResponse, LocalResponse
from mindee.error.mindee_error import MindeeApiV2Error, MindeeError
from mindee.error.mindee_http_error_v2 import MindeeHTTPErrorV2
from mindee.input import LocalInputSource, PathInput
from mindee.mindee_http.base_settings import USER_AGENT
from mindee.parsing.v2.inference import Inference
from mindee.parsing.v2.job import Job
from mindee.parsing.v2.job_response import JobResponse
from tests.test_inputs import FILE_TYPES_DIR, V2_DATA_DIR
from tests.utils import dummy_envvars


@pytest.fixture
def env_client(monkeypatch) -> ClientV2:
    dummy_envvars(monkeypatch)
    return ClientV2("dummy")


@pytest.fixture
def custom_base_url_client(monkeypatch) -> ClientV2:
    class _FakePostRespError:
        status_code = 400  # any non-2xx will do
        ok = False

        def json(self):
            # Shape must match what handle_error_v2 expects
            return {"status": -1, "detail": "forced failure from test"}

    class _FakeOkProcessingJobResp:
        status_code = 200
        ok = True

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
        ok = True

        def json(self):
            data_file = (
                V2_DATA_DIR / "products" / "financial_document" / "complete.json"
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
        "mindee.mindee_http.mindee_api_v2.MindeeApiV2.req_post_inference_enqueue",
        _fake_error_post_inference_enqueue,
        raising=True,
    )

    monkeypatch.setattr(
        "mindee.mindee_http.mindee_api_v2.MindeeApiV2.req_get_job",
        _fake_ok_get_job,
        raising=True,
    )

    monkeypatch.setattr(
        "mindee.mindee_http.mindee_api_v2.MindeeApiV2.req_get_inference",
        _fake_ok_get_inference,
        raising=True,
    )

    return ClientV2("dummy")


@pytest.mark.v2
def test_parse_path_without_token():
    with pytest.raises(MindeeApiV2Error):
        ClientV2()


@pytest.mark.v2
def test_enqueue_path_with_env_token(custom_base_url_client):
    assert custom_base_url_client.mindee_api.base_url == "https://dummy-url"
    assert custom_base_url_client.mindee_api.url_root == "https://dummy-url"
    assert custom_base_url_client.mindee_api.api_key == "dummy"
    assert custom_base_url_client.mindee_api.base_headers["Authorization"] == "dummy"
    assert custom_base_url_client.mindee_api.base_headers["User-Agent"] == USER_AGENT
    input_doc: LocalInputSource = custom_base_url_client.source_from_path(
        f"{FILE_TYPES_DIR}/receipt.jpg"
    )
    with pytest.raises(MindeeHTTPErrorV2):
        custom_base_url_client.enqueue_inference(
            input_doc, InferenceParameters("dummy-model")
        )


@pytest.mark.v2
def test_enqueue_and_parse_path_with_env_token(custom_base_url_client):
    input_doc: LocalInputSource = custom_base_url_client.source_from_path(
        f"{FILE_TYPES_DIR}/receipt.jpg"
    )
    with pytest.raises(MindeeHTTPErrorV2):
        custom_base_url_client.enqueue_and_get_inference(
            input_doc, InferenceParameters("dummy-model")
        )


def _assert_findoc_inference(response: InferenceResponse):
    # There are already detailed tests of the inference object.
    # Here we are just testing whether the client can load OK.
    assert isinstance(response, InferenceResponse)
    assert isinstance(response.inference, Inference)
    assert response.inference.id
    assert response.inference.model.id
    assert len(response.inference.result.fields) > 1


@pytest.mark.v2
def test_loads_from_prediction():
    input_inference = LocalResponse(
        V2_DATA_DIR / "products" / "financial_document" / "complete.json"
    )
    response = input_inference.deserialize_response(InferenceResponse)
    _assert_findoc_inference(response)
    with pytest.raises(MindeeError):
        input_inference.deserialize_response(JobResponse)


@pytest.mark.v2
def test_get_inference(custom_base_url_client):
    response = custom_base_url_client.get_inference(
        "12345678-1234-1234-1234-123456789ABC"
    )
    _assert_findoc_inference(response)


@pytest.mark.v2
def test_error_handling(custom_base_url_client):
    with pytest.raises(MindeeHTTPErrorV2) as e:
        custom_base_url_client.enqueue_inference(
            PathInput(
                V2_DATA_DIR / "products" / "financial_document" / "default_sample.jpg"
            ),
            InferenceParameters("dummy-model"),
        )
        assert e.status_code == -1
        assert e.detail == "forced failure from test"


@pytest.mark.v2
def test_enqueue(custom_base_url_client):
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
