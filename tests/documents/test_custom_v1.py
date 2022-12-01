import json

import pytest

from mindee.documents.custom.custom_v1 import CustomV1
from mindee.fields.api_builder import ClassificationField, ListField, ListFieldValue
from tests import CUSTOM_DATA_DIR

FILE_PATH_CUSTOM_V1_COMPLETE = f"{CUSTOM_DATA_DIR}/response_v1/complete.json"
FILE_PATH_CUSTOM_V1_EMPTY = f"{CUSTOM_DATA_DIR}/response_v1/empty.json"


@pytest.fixture
def custom_v1_doc_object():
    json_data = json.load(open(FILE_PATH_CUSTOM_V1_COMPLETE))
    return CustomV1(
        "field_test", api_prediction=json_data["document"]["inference"], page_n=None
    )


@pytest.fixture
def custom_v1_doc_object_empty():
    json_data = json.load(open(FILE_PATH_CUSTOM_V1_EMPTY))
    return CustomV1(
        "field_test", api_prediction=json_data["document"]["inference"], page_n=None
    )


@pytest.fixture
def custom_v1_page_object():
    json_data = json.load(open(FILE_PATH_CUSTOM_V1_COMPLETE))
    return CustomV1(
        "field_test", json_data["document"]["inference"]["pages"][0], page_n=0
    )


def test_empty(custom_v1_doc_object_empty):
    for field_name, field in custom_v1_doc_object_empty.fields.items():
        assert len(field_name) > 0
        assert isinstance(field, ListField)
        assert len(field.values) == 0
    for field_name, field in custom_v1_doc_object_empty.classifications.items():
        assert len(field_name) > 0
        assert isinstance(field, ClassificationField)
        assert field.value is None


def test_complete(custom_v1_doc_object):
    doc_str = open(f"{CUSTOM_DATA_DIR}/response_v1/doc_to_string.txt").read().strip()
    for field_name, field in custom_v1_doc_object.fields.items():
        assert len(field_name) > 0
        assert isinstance(field, ListField)
        assert len(field.values) > 0
        assert len(field.contents_list) == len(field.values)
        for value in field.values:
            assert isinstance(value, ListFieldValue)
            assert value.content != ""
            assert len(value.bounding_box) == 4
            assert value.confidence != 0.0
            assert field.page_n == 0 or field.page_n == 1
    for field_name, field in custom_v1_doc_object.classifications.items():
        assert len(field_name) > 0
        assert isinstance(field, ClassificationField)
        assert field.value != ""
    assert str(custom_v1_doc_object) == doc_str


def test_page_complete(custom_v1_page_object):
    assert custom_v1_page_object.orientation.value == 0
    for field_name, field in custom_v1_page_object.fields.items():
        assert isinstance(field, ListField)
        assert len(field.contents_list) == len(field.values)
        assert field.page_n == 0
