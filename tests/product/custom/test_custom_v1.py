import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.parsing.custom import ClassificationFieldV1, ListFieldV1, ListFieldValueV1
from mindee.product import CustomV1
from mindee.product.custom.custom_v1_document import CustomV1Document
from mindee.product.custom.custom_v1_page import CustomV1Page

CUSTOM_DATA_DIR = "./tests/data/products/custom"
FILE_PATH_CUSTOM_V1_COMPLETE = f"{CUSTOM_DATA_DIR}/response_v1/complete.json"
FILE_PATH_CUSTOM_V1_EMPTY = f"{CUSTOM_DATA_DIR}/response_v1/empty.json"
SUMMARY_FULL = f"{CUSTOM_DATA_DIR}/response_v1/summary_full.rst"
SUMMARY_PAGE_0 = f"{CUSTOM_DATA_DIR}/response_v1/summary_page0.rst"
SUMMARY_PAGE_1 = f"{CUSTOM_DATA_DIR}/response_v1/summary_page1.rst"


@pytest.fixture
def custom_v1_complete_doc():
    json_data = json.load(open(FILE_PATH_CUSTOM_V1_COMPLETE))
    return Document(CustomV1, json_data["document"])


@pytest.fixture
def custom_v1_empty_doc():
    json_data = json.load(open(FILE_PATH_CUSTOM_V1_EMPTY))
    return Document(CustomV1, json_data["document"])


@pytest.fixture
def custom_v1_page_0_object():
    json_data = json.load(open(FILE_PATH_CUSTOM_V1_COMPLETE))
    return Page(CustomV1Page, json_data["document"]["inference"]["pages"][0])


@pytest.fixture
def custom_v1_page_1_object():
    json_data = json.load(open(FILE_PATH_CUSTOM_V1_COMPLETE))
    return Page(CustomV1Page, json_data["document"]["inference"]["pages"][1])


def test_empty_doc(custom_v1_empty_doc):
    document_prediction: CustomV1Document = custom_v1_empty_doc.inference.prediction
    for field_name, field in document_prediction.fields.items():
        assert len(field_name) > 0
        assert isinstance(field, ListFieldV1)
        assert len(field.values) == 0
    for field_name, field in document_prediction.classifications.items():
        assert len(field_name) > 0
        assert isinstance(field, ClassificationFieldV1)
        assert field.value is None


def test_complete_doc(custom_v1_complete_doc):
    document_prediction: CustomV1Document = custom_v1_complete_doc.inference.prediction
    doc_str = open(SUMMARY_FULL).read()
    for field_name, field in document_prediction.fields.items():
        assert len(field_name) > 0
        assert isinstance(field, ListFieldV1)
        assert len(field.values) > 0
        assert len(field.contents_list) == len(field.values)
        for value in field.values:
            assert isinstance(value, ListFieldValueV1)
            assert value.content != ""
            assert len(value.bounding_box) == 4
            assert value.confidence != 0.0
    for field_name, field in document_prediction.classifications.items():
        assert len(field_name) > 0
        assert isinstance(field, ClassificationFieldV1)
        assert field.value != ""
    assert str(custom_v1_complete_doc) == doc_str


def test_complete_page_0(custom_v1_page_0_object):
    page_0_prediction = custom_v1_page_0_object.prediction
    page_0_str = open(SUMMARY_PAGE_0).read()
    assert custom_v1_page_0_object.orientation.value == 0
    assert len(custom_v1_page_0_object.extras.cropper.cropping) == 1
    for field_name, field in page_0_prediction.fields.items():
        assert isinstance(field, ListFieldV1)
        assert len(field.contents_list) == len(field.values)
        assert field.page_id == 0
    assert str(custom_v1_page_0_object) == page_0_str


def test_complete_page_1(custom_v1_page_1_object):
    page_1_prediction = custom_v1_page_1_object.prediction
    page_1_str = open(SUMMARY_PAGE_1).read()
    assert custom_v1_page_1_object.orientation.value == 0
    for field_name, field in page_1_prediction.fields.items():
        assert isinstance(field, ListFieldV1)
        assert len(field.contents_list) == len(field.values)
        assert field.page_id == 1
    assert str(custom_v1_page_1_object) == page_1_str
