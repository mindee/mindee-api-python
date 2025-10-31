import io

import pytest

from mindee.error.mimetype_error import MimeTypeError
from mindee.error.mindee_error import MindeeSourceError
from mindee.input.sources import (
    Base64Input,
    BytesInput,
    FileInput,
    LocalInputSource,
    PathInput,
    UrlInputSource,
)
from tests.utils import FILE_TYPES_DIR


def test_pdf_read_contents():
    input_source = PathInput(FILE_TYPES_DIR / "pdf" / "multipage.pdf")
    contents = input_source.read_contents(close_file=False)
    assert contents[0] == "multipage.pdf"
    assert isinstance(contents[1], bytes)
    assert not input_source.file_object.closed

    input_source.read_contents(close_file=True)
    assert input_source.file_object.closed


@pytest.mark.parametrize(
    ("filename", "page_count"),
    (
        ("multipage_cut-1.pdf", 1),
        ("multipage_cut-3.pdf", 3),
        ("multipage.pdf", 12),
    ),
)
def test_pdf_input_from_path(filename, page_count):
    input_source = PathInput(FILE_TYPES_DIR / "pdf" / filename)
    assert input_source.file_mimetype == "application/pdf"
    assert input_source.is_pdf() is True
    assert input_source.page_count == page_count
    assert isinstance(input_source.file_object, io.BufferedReader)


def test_pdf_input_from_url():
    with pytest.raises(MindeeSourceError):
        UrlInputSource(url="http://example.com/invoice.pdf")


TEST_IMAGES = (
    ("receipt.tif", "image/tiff"),
    ("receipt.tiff", "image/tiff"),
    ("receipt.jpg", "image/jpeg"),
    # invalid extensions won't be detected properly
    # ("receipt.jpga", "image/jpeg"),
    ("receipt.png", "image/png"),
    ("receipt.heic", "image/heic"),
)


def _assert_image(input_source: LocalInputSource, mimetype: str) -> None:
    assert input_source.file_mimetype == mimetype
    assert input_source.is_pdf() is False
    assert input_source.page_count == 1
    assert isinstance(input_source.file_object.read(15), bytes)


@pytest.mark.parametrize(("filename", "mimetype"), TEST_IMAGES)
def test_image_input_from_path(filename, mimetype):
    input_source = PathInput(FILE_TYPES_DIR / filename)
    _assert_image(input_source, mimetype)


@pytest.mark.parametrize(("filename", "mimetype"), TEST_IMAGES)
def test_image_input_from_file(filename, mimetype):
    with open(FILE_TYPES_DIR / filename, "rb") as fp:
        input_source = FileInput(fp)
        _assert_image(input_source, mimetype)


@pytest.mark.parametrize(("filename", "mimetype"), TEST_IMAGES)
def test_image_input_from_bytes(filename, mimetype):
    file_bytes = open(FILE_TYPES_DIR / filename, "rb").read()
    input_source = BytesInput(file_bytes, filename=filename)
    _assert_image(input_source, mimetype)


def test_image_input_from_base64():
    base64_input = open(FILE_TYPES_DIR / "receipt.txt", "r").read()
    input_source = Base64Input(base64_input, filename="receipt.jpg")
    _assert_image(input_source, mimetype="image/jpeg")


def test_txt_input_from_path():
    with pytest.raises(MimeTypeError):
        PathInput(FILE_TYPES_DIR / "receipt.txt")
