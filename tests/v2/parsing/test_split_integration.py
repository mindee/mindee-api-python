import os

import pytest

from mindee import ClientV2, PathInput
from mindee.input import UtilityParameters
from mindee.v2 import SplitResponse
from tests.utils import FILE_TYPES_DIR


@pytest.fixture(scope="session")
def split_model_id() -> str:
    """Identifier of the Financial Document model, supplied through an env var."""
    return os.getenv("MINDEE_V2_SPLIT_UTILITY_MODEL_ID")


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
    input_source = PathInput(FILE_TYPES_DIR / "pdf" / "blank_1.pdf")
    response = v2_client.enqueue_and_get_utility(
        SplitResponse, input_source, UtilityParameters(split_model_id)
    )
    assert response.inference is not None
    assert response.inference.file.name == "blank_1.pdf"
    assert response.inference.result.get("split")
    assert len(response.inference.result.get("split")) == 1
