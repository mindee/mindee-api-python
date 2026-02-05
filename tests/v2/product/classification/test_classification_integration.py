import os

import pytest

from mindee import ClientV2, PathInput
from mindee.v2 import ClassificationParameters, ClassificationResponse
from tests.utils import V2_UTILITIES_DATA_DIR


@pytest.fixture(scope="session")
def classification_model_id() -> str:
    """Identifier of the Financial Document model, supplied through an env var."""
    return os.getenv("MINDEE_V2_SE_TESTS_CLASSIFICATION_MODEL_ID")


@pytest.fixture(scope="session")
def v2_client() -> ClientV2:
    return ClientV2()


@pytest.mark.integration
@pytest.mark.v2
def test_classification_default_sample(
    v2_client: ClientV2, classification_model_id: str
):
    input_source = PathInput(
        V2_UTILITIES_DATA_DIR / "classification" / "default_invoice.jpg"
    )
    response = v2_client.enqueue_and_get_result(
        ClassificationResponse,
        input_source,
        ClassificationParameters(classification_model_id),
    )
    assert response.inference is not None
    assert response.inference.file.name == "default_invoice.jpg"
    assert response.inference.result.classification
    assert response.inference.result.classification.document_type == "invoice"
