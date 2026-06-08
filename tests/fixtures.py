import os

import pytest


@pytest.fixture(scope="session")
def findoc_model_id() -> str:
    """Identifier of the Financial Document model, supplied through an env var."""
    findoc_model_id = os.getenv("MINDEE_V2_SE_TESTS_FINDOC_MODEL_ID")
    if not findoc_model_id:
        raise ValueError(
            "MINDEE_V2_SE_TESTS_FINDOC_MODEL_ID environment variable is not set"
        )
    return findoc_model_id
