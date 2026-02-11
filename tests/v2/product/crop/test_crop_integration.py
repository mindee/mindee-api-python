import os

import pytest

from mindee import ClientV2, PathInput
from mindee.v2 import CropParameters, CropResponse
from tests.utils import V2_PRODUCT_DATA_DIR


@pytest.fixture(scope="session")
def crop_model_id() -> str:
    """Identifier of the Financial Document model, supplied through an env var."""
    return os.getenv("MINDEE_V2_SE_TESTS_CROP_MODEL_ID")


@pytest.fixture(scope="session")
def v2_client() -> ClientV2:
    return ClientV2()


@pytest.mark.integration
@pytest.mark.v2
def test_crop_default_sample(v2_client: ClientV2, crop_model_id: str):
    input_source = PathInput(V2_PRODUCT_DATA_DIR / "crop" / "default_sample.jpg")
    response = v2_client.enqueue_and_get_result(
        CropResponse, input_source, CropParameters(crop_model_id)
    )
    assert response.inference is not None
    assert response.inference.file.name == "default_sample.jpg"
    assert response.inference.result.crops
    assert len(response.inference.result.crops) == 2
