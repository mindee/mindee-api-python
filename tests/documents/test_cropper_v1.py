import json

import pytest

from mindee.documents.cropper.cropper_v1 import CropperV1
from tests import CROPPER_DATA_DIR

FILE_PATH_CROPPER_V1_COMPLETE = f"{CROPPER_DATA_DIR}/response_v1/complete.json"
FILE_PATH_CROPPER_V1_EMPTY = f"{CROPPER_DATA_DIR}/response_v1/empty.json"


@pytest.fixture
def cropper_v1_doc_object():
    json_data = json.load(open(FILE_PATH_CROPPER_V1_COMPLETE))
    return CropperV1(api_prediction=json_data["document"]["inference"], page_n=None)


@pytest.fixture
def cropper_v1_doc_object_empty():
    json_data = json.load(open(FILE_PATH_CROPPER_V1_EMPTY))
    return CropperV1(api_prediction=json_data["document"]["inference"], page_n=None)


@pytest.fixture
def cropper_v1_page_object():
    json_data = json.load(open(FILE_PATH_CROPPER_V1_COMPLETE))
    return CropperV1(json_data["document"]["inference"]["pages"][0], page_n=0)


def test_doc_constructor(cropper_v1_doc_object):
    doc_str = open(f"{CROPPER_DATA_DIR}/response_v1/doc_to_string.txt").read().strip()
    assert cropper_v1_doc_object.orientation is None
    assert str(cropper_v1_doc_object) == doc_str


def test_page_constructor(cropper_v1_page_object):
    doc_str = open(f"{CROPPER_DATA_DIR}/response_v1/page0_to_string.txt").read().strip()
    assert cropper_v1_page_object.orientation.value == 0
    assert str(cropper_v1_page_object) == doc_str
