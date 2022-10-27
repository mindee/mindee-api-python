import json

import pytest

from mindee.documents.custom.custom_v1 import CustomV1
from mindee.fields.api_builder import ClassificationField, ListField, ListFieldValue
from tests import CUSTOM_DATA_DIR

CUSTOM_FILE_PATH = f"{CUSTOM_DATA_DIR}/response_v1/complete.json"
CUSTOM_NA_FILE_PATH = f"{CUSTOM_DATA_DIR}/response_v1/empty.json"


@pytest.fixture
def custom_doc_object_complete():
    json_data = json.load(open(CUSTOM_FILE_PATH))
    return CustomV1(
        "field_test", json_data["document"]["inference"]["prediction"], page_n=None
    )


@pytest.fixture
def custom_doc_object_empty():
    json_data = json.load(open(CUSTOM_NA_FILE_PATH))
    return CustomV1(
        "field_test", json_data["document"]["inference"]["prediction"], page_n=None
    )


def test_empty(custom_doc_object_empty):
    for field_name, field in custom_doc_object_empty.fields.items():
        assert len(field_name) > 0
        assert isinstance(field, ListField)
        assert len(field.values) == 0
    for field_name, field in custom_doc_object_empty.classifications.items():
        assert len(field_name) > 0
        assert isinstance(field, ClassificationField)
        assert field.value == ""


def test_complete(custom_doc_object_complete):
    doc_str = open(f"{CUSTOM_DATA_DIR}/response_v1/doc_to_string.txt").read().strip()
    for field_name, field in custom_doc_object_complete.fields.items():
        assert len(field_name) > 0
        assert isinstance(field, ListField)
        assert len(field.values) > 0
        assert len(field.contents_list) == len(field.values)
        for value in field.values:
            assert isinstance(value, ListFieldValue)
            assert value.content != ""
            assert len(value.bounding_box) == 4
            assert value.confidence != 0.0
    for field_name, field in custom_doc_object_complete.classifications.items():
        assert len(field_name) > 0
        assert isinstance(field, ClassificationField)
        assert field.value != ""
    assert str(custom_doc_object_complete) == doc_str
