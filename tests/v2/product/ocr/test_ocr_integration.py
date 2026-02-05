import os

import pytest

from mindee import ClientV2, PathInput
from mindee.v2 import OCRParameters, OCRResponse
from mindee.v2.product.ocr import OCRInference, OCRResult
from tests.utils import V2_UTILITIES_DATA_DIR


@pytest.fixture(scope="session")
def ocr_model_id() -> str:
    """Identifier of the Financial Document model, supplied through an env var."""
    return os.getenv("MINDEE_V2_SE_TESTS_OCR_MODEL_ID")


@pytest.fixture(scope="session")
def v2_client() -> ClientV2:
    return ClientV2()


@pytest.mark.integration
@pytest.mark.v2
def test_ocr_default_sample(v2_client: ClientV2, ocr_model_id: str):
    input_source = PathInput(V2_UTILITIES_DATA_DIR / "ocr" / "default_sample.jpg")
    response = v2_client.enqueue_and_get_result(
        OCRResponse, input_source, OCRParameters(ocr_model_id)
    )
    assert response.inference is not None
    assert response.inference.file.name == "default_sample.jpg"
    assert isinstance(response.inference, OCRInference)
    assert isinstance(response.inference.result, OCRResult)
    assert len(response.inference.result.pages) == 1
    assert len(response.inference.result.pages[0].words) > 5
