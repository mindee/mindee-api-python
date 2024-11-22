import json

import pytest

from mindee.geometry.quadrilateral import Quadrilateral
from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.parsing.custom.classification import ClassificationField
from mindee.parsing.custom.list import ListField, ListFieldValue
from mindee.product.custom.custom_v1 import CustomV1
from mindee.product.custom.custom_v1_document import CustomV1Document
from mindee.product.custom.custom_v1_page import CustomV1Page
from tests.product import PRODUCT_DATA_DIR


@pytest.fixture
def custom_v1_complete_doc() -> Document[CustomV1Document, Page[CustomV1Page]]:
    json_data = json.load(
        open(PRODUCT_DATA_DIR / "custom" / "response_v2" / "complete.json")
    )
    return Document(CustomV1, json_data["document"])


@pytest.fixture
def custom_v1_empty_doc() -> Document[CustomV1Document, Page[CustomV1Page]]:
    json_data = json.load(
        open(PRODUCT_DATA_DIR / "custom" / "response_v2" / "empty.json")
    )

    return Document(CustomV1, json_data["document"])


@pytest.fixture
def custom_v1_complete_page_0() -> Page[CustomV1Page]:
    json_data = json.load(
        open(PRODUCT_DATA_DIR / "custom" / "response_v2" / "complete.json")
    )

    return Page(CustomV1Page, json_data["document"]["inference"]["pages"][0])


@pytest.fixture
def custom_v1_complete_page_1() -> Page[CustomV1Page]:
    json_data = json.load(
        open(PRODUCT_DATA_DIR / "custom" / "response_v2" / "complete.json")
    )

    return Page(CustomV1Page, json_data["document"]["inference"]["pages"][1])


def test_empty_doc(custom_v1_empty_doc) -> None:
    document_prediction: CustomV1Document = custom_v1_empty_doc.inference.prediction
    for field_name, field in document_prediction.fields.items():
        assert len(field_name) > 0
        assert isinstance(field, ListField)
        assert len(field.values) == 0
    for (
        classification_name,
        classification,
    ) in document_prediction.classifications.items():
        assert len(classification_name) > 0
        assert isinstance(classification, ClassificationField)
        assert classification.value is None


def test_complete_doc(custom_v1_complete_doc) -> None:
    document_prediction: CustomV1Document = custom_v1_complete_doc.inference.prediction
    doc_str = open(
        PRODUCT_DATA_DIR / "custom" / "response_v2" / "summary_full.rst"
    ).read()
    for field_name, field in document_prediction.fields.items():
        assert len(field_name) > 0
        assert isinstance(field, ListField)
        assert len(field.values) > 0
        assert len(field.contents_list) == len(field.values)
        for value in field.values:
            assert isinstance(value, ListFieldValue)
            assert value.content != ""
            assert isinstance(value.bounding_box, Quadrilateral)
            assert len(value.bounding_box) == 4
            assert value.confidence != 0.0
    for (
        classification_name,
        classification,
    ) in document_prediction.classifications.items():
        assert len(classification_name) > 0
        assert isinstance(classification, ClassificationField)
        assert classification.value != ""
    assert str(custom_v1_complete_doc) == doc_str


def test_complete_page_0(custom_v1_complete_page_0):
    page_0_prediction = custom_v1_complete_page_0.prediction
    page_0_str = open(
        PRODUCT_DATA_DIR / "custom" / "response_v2" / "summary_page0.rst"
    ).read()
    assert custom_v1_complete_page_0.orientation.value == 0
    assert len(custom_v1_complete_page_0.extras.cropper.cropping) == 1
    for field in page_0_prediction.fields.values():
        assert isinstance(field, ListField)
        assert len(field.contents_list) == len(field.values)
        for value in field.values:
            assert value.page_id == 0
    assert str(custom_v1_complete_page_0) == page_0_str


def test_complete_page_1(custom_v1_complete_page_1):
    page_1_prediction = custom_v1_complete_page_1.prediction
    page_1_str = open(
        PRODUCT_DATA_DIR / "custom" / "response_v2" / "summary_page1.rst"
    ).read()
    assert custom_v1_complete_page_1.orientation.value == 0
    for field in page_1_prediction.fields.values():
        assert isinstance(field, ListField)
        assert len(field.contents_list) == len(field.values)
        for value in field.values:
            assert value.page_id == 1
    assert str(custom_v1_complete_page_1) == page_1_str
