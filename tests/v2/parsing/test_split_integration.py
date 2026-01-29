import os

import pytest

from mindee import ClientV2, PathInput
from mindee.input import SplitParameters
from mindee.v2 import SplitResponse
from tests.utils import V1_PRODUCT_DATA_DIR


@pytest.fixture(scope="session")
def split_model_id() -> str:
    """Identifier of the Financial Document model, supplied through an env var."""
    return os.getenv("MINDEE_V2_SE_TESTS_SPLIT_MODEL_ID")


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
def test_split_blank(v2_client: ClientV2, split_model_id: str):
    input_source = PathInput(
        V1_PRODUCT_DATA_DIR / "invoice_splitter" / "default_sample.pdf"
    )
    response = v2_client.enqueue_and_get_result(
        SplitResponse, input_source, SplitParameters(split_model_id)
    )  # Note: do not use blank_1.pdf for this.
    assert response.inference is not None
    assert response.inference.file.name == "default_sample.pdf"
    assert response.inference.result.get("split")
    assert len(response.inference.result.get("split")) == 2
