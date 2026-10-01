import os

import pytest

from mindee.v2 import Client


@pytest.fixture(scope="session")
def v2_client() -> Client:
    return Client()


@pytest.fixture(scope="session")
def findoc_model_id() -> str:
    """Identifier of the Financial Document model, supplied through an env var."""
    findoc_model_id = os.getenv("MINDEE_V2_SE_TESTS_FINDOC_MODEL_ID", "")
    if findoc_model_id is None:
        raise ValueError(
            "MINDEE_V2_SE_TESTS_FINDOC_MODEL_ID environment variable is not set"
        )
    return findoc_model_id


@pytest.fixture(scope="session")
def split_model_id() -> str:
    """Identifier of the Split model, supplied through an env var."""
    split_model_id = os.getenv("MINDEE_V2_SE_TESTS_SPLIT_MODEL_ID", "")
    if split_model_id is None:
        raise ValueError(
            "MINDEE_V2_SE_TESTS_SPLIT_MODEL_ID environment variable is not set"
        )
    return split_model_id


@pytest.fixture(scope="session")
def crop_model_id() -> str:
    """Identifier of the Financial Document model, supplied through an env var."""
    crop_model_id = os.getenv("MINDEE_V2_SE_TESTS_CROP_MODEL_ID")
    if crop_model_id is None:
        raise ValueError(
            "MINDEE_V2_SE_TESTS_CROP_MODEL_ID environment variable is not set"
        )
    return crop_model_id
