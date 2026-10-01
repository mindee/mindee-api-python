import pytest

from mindee.error.mindee_error import MindeeSourceError
from mindee.input.url_input_source import URLInputSource


def test_rejects_http():
    with pytest.raises(MindeeSourceError, match="HTTPS"):
        URLInputSource("http://example.com/file.pdf")


def test_rejects_ftp():
    with pytest.raises(MindeeSourceError, match="HTTPS"):
        URLInputSource("ftp://example.com/file.pdf")


def test_accepts_https():
    input_source = URLInputSource("https://example.com/file.pdf")
    assert input_source.url
