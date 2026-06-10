import pytest

from mindee.dependencies import PILLOW_AVAILABLE, PYPDFIUM2_AVAILABLE


@pytest.mark.pillow
def test_pillow_installed():
    assert PILLOW_AVAILABLE


@pytest.mark.pypdfium2
def test_pypdfium2_installed():
    assert PYPDFIUM2_AVAILABLE


@pytest.mark.lite
def test_pillow_missing():
    assert not PILLOW_AVAILABLE


@pytest.mark.lite
def test_pypdfium2_missing():
    assert not PYPDFIUM2_AVAILABLE
