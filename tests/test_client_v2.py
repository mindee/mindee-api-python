import pytest

from mindee import ClientV2, InferencePredictOptions, LocalResponse
from mindee.error.mindee_error import MindeeApiV2Error
from mindee.error.mindee_http_error_v2 import MindeeHTTPErrorV2
from mindee.input import LocalInputSource, PathInput
from mindee.mindee_http.base_settings import USER_AGENT
from tests.test_inputs import FILE_TYPES_DIR, V2_DATA_DIR
from tests.utils import dummy_envvars


@pytest.fixture
def env_client(monkeypatch) -> ClientV2:
    dummy_envvars(monkeypatch)
    return ClientV2("dummy")


@pytest.fixture
def custom_base_url_client(monkeypatch) -> ClientV2:
    class _FakeResp:
        status_code = 400  # any non-2xx will do
        ok = False

        def json(self):
            # Shape must match what handle_error_v2 expects
            return {"status": -1, "detail": "forced failure from test"}

    monkeypatch.setenv("MINDEE_V2_BASE_URL", "https://dummy-url")

    def _fake_response(*args, **kwargs):
        return _FakeResp()

    monkeypatch.setattr(
        "mindee.mindee_http.mindee_api_v2.requests.post",
        _fake_response,
        raising=True,
    )

    monkeypatch.setattr(
        "mindee.mindee_http.mindee_api_v2.requests.get",
        _fake_response,
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
        custom_base_url_client.enqueue(
            input_doc, InferencePredictOptions("dummy-model")
        )


@pytest.mark.v2
def test_enqueue_and_parse_path_with_env_token(custom_base_url_client):
    input_doc: LocalInputSource = custom_base_url_client.source_from_path(
        f"{FILE_TYPES_DIR}/receipt.jpg"
    )
    with pytest.raises(MindeeHTTPErrorV2):
        custom_base_url_client.enqueue_and_parse(
            input_doc, InferencePredictOptions("dummy-model")
        )


@pytest.mark.v2
def test_parse_queued6_and_parse_path_with_env_token(custom_base_url_client):
    with pytest.raises(MindeeHTTPErrorV2):
        custom_base_url_client.parse_queued("dummy-queue")


@pytest.mark.v2
def test_loads_from_prediction(env_client):
    input_inference = LocalResponse(
        V2_DATA_DIR / "products" / "financial_document" / "complete.json"
    )
    prediction = env_client.load_inference(input_inference)
    assert prediction.inference.model.id == "12345678-1234-1234-1234-123456789abc"


@pytest.mark.v2
def test_error_handling(custom_base_url_client):
    with pytest.raises(MindeeHTTPErrorV2) as e:
        custom_base_url_client.enqueue(
            PathInput(
                V2_DATA_DIR / "products" / "financial_document" / "default_sample.jpg"
            ),
            InferencePredictOptions("dummy-model"),
        )
        assert e.status_code == -1
        assert e.detail == "forced failure from test"
