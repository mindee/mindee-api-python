from pathlib import Path

import pytest

from mindee.input.local_response import LocalResponse
from tests.api.test_async_response import ASYNC_DIR


@pytest.fixture
def dummy_secret_key():
    return "ogNjY44MhvKPGTtVsI8zG82JqWQa68woYQH"


@pytest.fixture
def signature():
    return "5ed1673e34421217a5dbfcad905ee62261a3dd66c442f3edd19302072bbf70d0"


@pytest.fixture
def file_path():
    return Path(ASYNC_DIR / "get_completed_empty.json")


def test_valid_file_local_response(dummy_secret_key, signature, file_path):
    with open(file_path, "rb") as file:
        local_response = LocalResponse(file)
    assert local_response._file is not None
    assert not local_response.is_valid_hmac_signature(
        dummy_secret_key, "invalid signature"
    )
    assert signature == local_response.get_hmac_signature(dummy_secret_key)
    assert local_response.is_valid_hmac_signature(dummy_secret_key, signature)


def test_valid_path_local_response(dummy_secret_key, signature, file_path):
    local_response = LocalResponse(file_path)
    assert local_response._file is not None
    assert not local_response.is_valid_hmac_signature(
        dummy_secret_key, "invalid signature"
    )
    assert signature == local_response.get_hmac_signature(dummy_secret_key)
    assert local_response.is_valid_hmac_signature(dummy_secret_key, signature)


def test_valid_bytes_local_response(dummy_secret_key, signature, file_path):
    with open(file_path, "r") as f:
        str_response = f.read().replace("\r", "").replace("\n", "")
    file_bytes = str_response.encode("utf-8")
    local_response = LocalResponse(file_bytes)
    assert local_response._file is not None
    assert not local_response.is_valid_hmac_signature(
        dummy_secret_key, "invalid signature"
    )
    assert signature == local_response.get_hmac_signature(dummy_secret_key)
    assert local_response.is_valid_hmac_signature(dummy_secret_key, signature)
