import gc
import os

import pytest


@pytest.fixture(autouse=True)
def force_gc():
    yield
    gc.collect()


@pytest.fixture(scope="session")
def findoc_model_id() -> str:
    """Identifier of the Financial Document model, supplied through an env var."""
    return os.getenv("MINDEE_V2_SE_TESTS_FINDOC_MODEL_ID", "")
