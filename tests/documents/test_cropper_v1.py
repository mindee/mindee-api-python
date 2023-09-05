import json

import pytest

from mindee.documents import CropperV1

CROPPER_DATA_DIR = "./tests/data/products/cropper"
FILE_PATH_CROPPER_V1_COMPLETE = f"{ CROPPER_DATA_DIR }/response_v1/complete.json"
FILE_PATH_CROPPER_V1_EMPTY = f"{ CROPPER_DATA_DIR }/response_v1/empty.json"


@pytest.fixture
def cropper_v1_doc() -> CropperV1:
    json_data = json.load(open(FILE_PATH_CROPPER_V1_COMPLETE))
    return CropperV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def cropper_v1_doc_empty() -> CropperV1:
    json_data = json.load(open(FILE_PATH_CROPPER_V1_EMPTY))
    return CropperV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def cropper_v1_page0():
    json_data = json.load(open(FILE_PATH_CROPPER_V1_COMPLETE))
    return CropperV1(json_data["document"]["inference"]["pages"][0], page_n=0)


def test_empty_doc_constructor(cropper_v1_doc_empty):
    assert len(cropper_v1_doc_empty.cropping) == 0


def test_doc_constructor(cropper_v1_doc):
    file_path = f"{ CROPPER_DATA_DIR }/response_v1/doc_to_string.rst"
    reference_str = open(file_path, "r", encoding="utf-8").read()
    assert str(cropper_v1_doc) == reference_str


def test_page0_constructor(cropper_v1_page0):
    file_path = f"{ CROPPER_DATA_DIR }/response_v1/page0_to_string.rst"
    reference_str = open(file_path, "r", encoding="utf-8").read()
    assert str(cropper_v1_page0) == reference_str
