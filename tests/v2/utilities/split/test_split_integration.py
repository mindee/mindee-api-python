import os

import pytest

from mindee import ClientV2, PathInput
from mindee.v2 import SplitParameters, SplitResponse
from tests.utils import V2_UTILITIES_DATA_DIR


@pytest.fixture(scope="session")
def split_model_id() -> str:
    """Identifier of the Financial Document model, supplied through an env var."""
    return os.getenv("MINDEE_V2_SE_TESTS_SPLIT_MODEL_ID")


@pytest.fixture(scope="session")
def v2_client() -> ClientV2:
    return ClientV2()


@pytest.mark.integration
@pytest.mark.v2
def test_split_blank(v2_client: ClientV2, split_model_id: str):
    input_source = PathInput(V2_UTILITIES_DATA_DIR / "split" / "default_sample.pdf")
    response = v2_client.enqueue_and_get_result(
        SplitResponse, input_source, SplitParameters(split_model_id)
    )
    assert response.inference is not None
    assert response.inference.file.name == "default_sample.pdf"
    assert response.inference.result.splits
    assert len(response.inference.result.splits) == 2
