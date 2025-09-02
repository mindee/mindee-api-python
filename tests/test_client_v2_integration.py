from __future__ import annotations

import os
from pathlib import Path

import pytest

from mindee import ClientV2, InferenceParameters, PathInput, UrlInputSource
from mindee.error.mindee_http_error_v2 import MindeeHTTPErrorV2
from mindee.parsing.v2.inference_response import InferenceResponse
from tests.test_inputs import FILE_TYPES_DIR, PRODUCT_DATA_DIR


@pytest.fixture(scope="session")
def findoc_model_id() -> str:
    """Identifier of the Financial Document model, supplied through an env var."""
    return os.getenv("MINDEE_V2_FINDOC_MODEL_ID")


@pytest.fixture(scope="session")
def v2_client() -> ClientV2:
    """
    Real V2 client configured with the user-supplied API key
    (or skipped when the key is absent).
    """
    api_key = os.getenv("MINDEE_V2_API_KEY")
    return ClientV2(api_key)


@pytest.mark.integration
@pytest.mark.v2
def test_parse_file_empty_multiple_pages_must_succeed(
    v2_client: ClientV2, findoc_model_id: str
) -> None:
    """
    Upload a 2-page blank PDF and make sure the returned inference contains the
    file & model metadata.
    """
    input_path: Path = FILE_TYPES_DIR / "pdf" / "multipage_cut-2.pdf"

    input_source = PathInput(input_path)
    params = InferenceParameters(
        model_id=findoc_model_id,
        rag=False,
        raw_text=True,
        polygon=False,
        confidence=False,
        webhook_ids=[],
        alias="py_integration_empty_multiple",
    )

    response: InferenceResponse = v2_client.enqueue_and_get_inference(
        input_source, params
    )

    assert response is not None
    assert response.inference is not None

    assert response.inference.file is not None
    assert response.inference.file.name == "multipage_cut-2.pdf"
    assert response.inference.file.page_count == 2

    assert response.inference.model is not None
    assert response.inference.model.id == findoc_model_id

    assert response.inference.active_options is not None
    assert response.inference.active_options.rag is False
    assert response.inference.active_options.raw_text is True
    assert response.inference.active_options.polygon is False
    assert response.inference.active_options.confidence is False

    assert response.inference.result.raw_text is not None
    assert len(response.inference.result.raw_text.pages) == 2


@pytest.mark.integration
@pytest.mark.v2
def test_parse_file_filled_single_page_must_succeed(
    v2_client: ClientV2, findoc_model_id: str
) -> None:
    """
    Upload a filled single-page JPEG and verify that common fields are present.
    """
    input_path: Path = PRODUCT_DATA_DIR / "financial_document" / "default_sample.jpg"

    input_source = PathInput(input_path)
    params = InferenceParameters(
        model_id=findoc_model_id,
        rag=False,
        raw_text=False,
        polygon=False,
        confidence=False,
        webhook_ids=[],
        alias="py_integration_filled_single",
    )

    response: InferenceResponse = v2_client.enqueue_and_get_inference(
        input_source, params
    )

    assert response is not None
    assert response.inference is not None

    assert response.inference.file is not None
    assert response.inference.file.name == "default_sample.jpg"
    assert response.inference.file.page_count == 1

    assert response.inference.model is not None
    assert response.inference.model.id == findoc_model_id

    assert response.inference.active_options is not None
    assert response.inference.active_options.rag is False
    assert response.inference.active_options.raw_text is False
    assert response.inference.active_options.polygon is False
    assert response.inference.active_options.confidence is False

    assert response.inference.result.raw_text is None

    assert response.inference.result is not None
    supplier_name = response.inference.result.fields["supplier_name"]
    assert supplier_name is not None
    assert supplier_name.value == "John Smith"
    assert supplier_name.confidence is None
    assert len(supplier_name.locations) == 0


@pytest.mark.integration
@pytest.mark.v2
def test_invalid_uuid_must_throw_error_422(v2_client: ClientV2) -> None:
    """
    Using an invalid model identifier must trigger a 422 HTTP error.
    """
    input_path: Path = FILE_TYPES_DIR / "pdf" / "multipage_cut-2.pdf"

    input_source = PathInput(input_path)
    params = InferenceParameters(model_id="INVALID MODEL ID")

    with pytest.raises(MindeeHTTPErrorV2) as exc_info:
        v2_client.enqueue_inference(input_source, params)

    exc: MindeeHTTPErrorV2 = exc_info.value
    assert exc.status == 422


@pytest.mark.integration
@pytest.mark.v2
def test_url_input_source_must_not_raise_errors(
    v2_client: ClientV2,
    findoc_model_id: str,
) -> None:
    """
    Load a blank PDF from an HTTPS URL and make sure the inference call completes without raising any errors.
    """
    url = os.getenv("MINDEE_V2_SE_TESTS_BLANK_PDF_URL")

    input_source = UrlInputSource(url)
    params = InferenceParameters(
        model_id=findoc_model_id,
        rag=False,
        raw_text=False,
        polygon=False,
        confidence=False,
        webhook_ids=[],
        alias="py_integration_url_source",
    )
    response: InferenceResponse = v2_client.enqueue_and_get_inference(
        input_source, params
    )
    assert response is not None
    assert response.inference is not None
