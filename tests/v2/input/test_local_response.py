from pathlib import Path

import pytest

from mindee import InferenceResponse
from mindee.input import LocalResponse
from tests.utils import V2_DATA_DIR


@pytest.fixture
def file_path() -> Path:
    return V2_DATA_DIR / "inference" / "standard_field_types.json"


def _assert_local_response(local_response):
    fake_hmac_signing = "ogNjY44MhvKPGTtVsI8zG82JqWQa68woYQH"
    signature = "a1bc9012fa63539d602f163d8980604a0cf2b2ae88e56009cfa1db33382736cf"

    assert local_response._file is not None
    assert not local_response.is_valid_hmac_signature(
        fake_hmac_signing, "invalid signature"
    )
    assert signature == local_response.get_hmac_signature(fake_hmac_signing)
    assert local_response.is_valid_hmac_signature(fake_hmac_signing, signature)
    reponse: InferenceResponse = local_response.deserialize_response(InferenceResponse)
    assert isinstance(reponse, InferenceResponse)
    assert reponse.inference is not None
    assert reponse.inference.result is not None
    assert reponse.inference.result.fields is not None


def test_valid_file_local_response(file_path):
    with open(file_path, "rb") as file:
        local_response = LocalResponse(file)
    _assert_local_response(local_response)


def test_valid_path_local_response(file_path):
    local_response = LocalResponse(file_path)
    assert local_response._file is not None
    _assert_local_response(local_response)


def test_valid_bytes_local_response(file_path):
    with open(file_path, "r") as f:
        str_response = f.read().replace("\r", "").replace("\n", "")
    file_bytes = str_response.encode("utf-8")
    local_response = LocalResponse(file_bytes)
    _assert_local_response(local_response)
