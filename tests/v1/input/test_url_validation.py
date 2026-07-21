import pytest

from mindee.error.mindee_error import MindeeSourceError
from mindee.mindee_http.response_validation import validate_url_for_source


class TestValidateUrlScheme:
    def test_rejects_http(self):
        with pytest.raises(MindeeSourceError, match="HTTPS"):
            validate_url_for_source("http://example.com/file.pdf")

    def test_rejects_ftp(self):
        with pytest.raises(MindeeSourceError, match="HTTPS"):
            validate_url_for_source("ftp://example.com/file.pdf")

    def test_accepts_https(self):
        validate_url_for_source("https://example.com/file.pdf")
