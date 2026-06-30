import pytest

from mindee.dependencies import PILLOW_AVAILABLE, BERNARD_LEDIT_AVAILABLE


@pytest.mark.pillow
def test_pillow_installed():
    assert PILLOW_AVAILABLE


@pytest.mark.bernard_ledit
def test_bernard_installed():
    assert BERNARD_LEDIT_AVAILABLE


@pytest.mark.lite
def test_pillow_missing():
    assert not PILLOW_AVAILABLE


@pytest.mark.lite
def test_bernard_missing():
    assert not BERNARD_LEDIT_AVAILABLE
