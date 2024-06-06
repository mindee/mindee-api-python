from io import BytesIO

import pytest

from mindee.error import MimeTypeError
from mindee.image_extraction.common import get_image_size
from tests.test_inputs import FILE_TYPES_DIR


@pytest.fixture
def jpg_file_path():
    return FILE_TYPES_DIR / "receipt.jpg"


@pytest.fixture
def txt_file_path():
    return FILE_TYPES_DIR / "receipt.txt"


@pytest.fixture
def png_file_path():
    return FILE_TYPES_DIR / "receipt.png"


def test_get_image_size_jpg(jpg_file_path):
    with open(jpg_file_path, "rb") as f:
        jpg_file = BytesIO(f.read())
    jpg_height, jpg_width = get_image_size(jpg_file)
    assert jpg_height == 800
    assert jpg_width == 1066


def test_get_image_size_png(png_file_path):
    with open(png_file_path, "rb") as f:
        png_file = BytesIO(f.read())
    png_height, png_width = get_image_size(png_file)
    assert png_height == 800
    assert png_width == 1066


def test_get_image_size_with_invalid_mime(txt_file_path):
    with open(txt_file_path, "rb") as f:
        txt_file = BytesIO(f.read())

    with pytest.raises(MimeTypeError):
        get_image_size(txt_file)
