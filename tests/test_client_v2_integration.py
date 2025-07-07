from __future__ import annotations

import os
from pathlib import Path

import pytest

from mindee import ClientV2, InferencePredictOptions
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
    assert input_path.exists(), f"sample file missing: {input_path}"

    input_doc = v2_client.source_from_path(input_path)
    options = InferencePredictOptions(findoc_model_id)

    response: InferenceResponse = v2_client.enqueue_and_parse(input_doc, options)

    assert response is not None
    assert response.inference is not None

    assert response.inference.file is not None
    assert response.inference.file.name == "multipage_cut-2.pdf"

    assert response.inference.model is not None
    assert response.inference.model.id == findoc_model_id


@pytest.mark.integration
@pytest.mark.v2
def test_parse_file_filled_single_page_must_succeed(
    v2_client: ClientV2, findoc_model_id: str
) -> None:
    """
    Upload a filled single-page JPEG and verify that common fields are present.
    """
    input_path: Path = PRODUCT_DATA_DIR / "financial_document" / "default_sample.jpg"
    assert input_path.exists(), f"sample file missing: {input_path}"

    input_doc = v2_client.source_from_path(input_path)
    options = InferencePredictOptions(findoc_model_id)

    response: InferenceResponse = v2_client.enqueue_and_parse(input_doc, options)

    assert response is not None
    assert response.inference is not None

    assert response.inference.file is not None
    assert response.inference.file.name == "default_sample.jpg"

    assert response.inference.model is not None
    assert response.inference.model.id == findoc_model_id

    assert response.inference.result is not None
    supplier_name = response.inference.result.fields["supplier_name"]
    assert supplier_name is not None
    assert supplier_name.value == "John Smith"


@pytest.mark.integration
@pytest.mark.v2
def test_invalid_uuid_must_throw_error_422(v2_client: ClientV2) -> None:
    """
    Using an invalid model identifier must trigger a 422 HTTP error.
    """
    input_path: Path = FILE_TYPES_DIR / "pdf" / "multipage_cut-2.pdf"
    assert input_path.exists()

    input_doc = v2_client.source_from_path(input_path)
    options = InferencePredictOptions("INVALID MODEL ID")

    with pytest.raises(MindeeHTTPErrorV2) as exc_info:
        v2_client.enqueue(input_doc, options)

    exc: MindeeHTTPErrorV2 = exc_info.value
    assert exc.status == 422
