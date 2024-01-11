import json

import pytest

from mindee.geometry.quadrilateral import Quadrilateral
from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.parsing.custom import GeneratedListField
from mindee.product.generated.generated_v1 import GeneratedV1
from mindee.product.generated.generated_v1_document import GeneratedV1Document
from mindee.product.generated.generated_v1_page import GeneratedV1Page
from tests.product import PRODUCT_DATA_DIR


@pytest.fixture
def international_id_v1_complete_doc() -> (
    Document[GeneratedV1Document, Page[GeneratedV1Page]]
):
    json_data = json.load(
        open(PRODUCT_DATA_DIR / "international_id" / "response_v1" / "complete.json")
    )
    return Document(GeneratedV1, json_data["document"])


@pytest.fixture
def international_id_v1_empty_doc() -> (
    Document[GeneratedV1Document, Page[GeneratedV1Page]]
):
    json_data = json.load(
        open(PRODUCT_DATA_DIR / "international_id" / "response_v1" / "empty.json")
    )

    return Document(GeneratedV1, json_data["document"])


@pytest.fixture
def international_id_v1_complete_page_0() -> Page[GeneratedV1Page]:
    json_data = json.load(
        open(PRODUCT_DATA_DIR / "international_id" / "response_v1" / "complete.json")
    )

    return Page(GeneratedV1Page, json_data["document"]["inference"]["pages"][0])


@pytest.fixture
def international_id_v1_complete_page_1() -> Page[GeneratedV1Page]:
    json_data = json.load(
        open(PRODUCT_DATA_DIR / "international_id" / "response_v1" / "complete.json")
    )

    return Page(GeneratedV1Page, json_data["document"]["inference"]["pages"][1])


def test_empty_doc(international_id_v1_empty_doc) -> None:
    document_prediction: GeneratedV1Document = (
        international_id_v1_empty_doc.inference.prediction
    )
    # TODO


def test_complete_doc(international_id_v1_complete_doc) -> None:
    document_prediction: GeneratedV1Document = (
        international_id_v1_complete_doc.inference.prediction
    )
    doc_str = open(
        PRODUCT_DATA_DIR / "international_id" / "response_v1" / "summary_full.rst"
    ).read()
    # TODO


def test_complete_page_0(international_id_v1_complete_page_0):
    page_0_prediction = international_id_v1_complete_page_0.prediction
    page_0_str = open(
        PRODUCT_DATA_DIR / "international_id" / "response_v1" / "summary_page0.rst"
    ).read()
    # TODO


def test_complete_page_1(international_id_v1_complete_page_1):
    page_1_prediction = international_id_v1_complete_page_1.prediction
    page_1_str = open(
        PRODUCT_DATA_DIR / "international_id" / "response_v1" / "summary_page1.rst"
    ).read()
    # TODO
