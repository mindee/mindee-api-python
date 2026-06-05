import gc

import pytest


@pytest.fixture(autouse=True)
def force_gc():
    yield
    gc.collect()
