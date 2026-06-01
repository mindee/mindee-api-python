from pathlib import Path

import pytest

from mindee.input import LocalResponse
from tests.v1.api.test_async_response import ASYNC_DIR


@pytest.fixture
def file_path() -> Path:
    return ASYNC_DIR / "get_completed_empty.json"


def _assert_local_response(local_response):
    fake_hmac_signing = "ogNjY44MhvKPGTtVsI8zG82JqWQa68woYQH"
    signature = "5ed1673e34421217a5dbfcad905ee62261a3dd66c442f3edd19302072bbf70d0"
    assert local_response._file is not None
    assert not local_response.is_valid_hmac_signature(
        fake_hmac_signing, "invalid signature"
    )
    assert signature == local_response.get_hmac_signature(fake_hmac_signing)
    assert local_response.is_valid_hmac_signature(fake_hmac_signing, signature)


def test_valid_file_local_response(file_path):
    with open(file_path, "rb") as file:
        local_response = LocalResponse(file)
    _assert_local_response(local_response)


def test_valid_path_local_response(file_path):
    local_response = LocalResponse(file_path)
    assert local_response._file is not None
    _assert_local_response(local_response)


def test_valid_bytes_local_response(file_path):
    with open(file_path) as f:
        str_response = f.read().replace("\r", "").replace("\n", "")
    file_bytes = str_response.encode("utf-8")
    local_response = LocalResponse(file_bytes)
    _assert_local_response(local_response)
