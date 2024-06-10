from io import BytesIO

import pytest
from PIL import Image

from mindee.error import MimeTypeError
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
        jpg_file = Image.open(jpg_file_path)
    jpg_height = jpg_file.size[0]
    jpg_width = jpg_file.size[1]
    assert jpg_height == 800
    assert jpg_width == 1066


def test_get_image_size_png(png_file_path):
    with open(png_file_path, "rb") as f:
        png_file = Image.open(png_file_path)
    png_height = png_file.size[0]
    png_width = png_file.size[1]
    assert png_height == 800
    assert png_width == 1066
