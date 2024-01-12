import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.generated.generated_v1 import GeneratedV1
from mindee.product.generated.generated_v1_document import GeneratedV1Document
from mindee.product.generated.generated_v1_page import GeneratedV1Page
from tests.product import PRODUCT_DATA_DIR


@pytest.fixture
def international_id_v1_complete_doc() -> (
    Document[GeneratedV1Document, Page[GeneratedV1Page]]
):
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR
            / "generated"
            / "response_v1"
            / "complete_international_id_v1.json"
        )
    )
    return Document(GeneratedV1, json_data["document"])


@pytest.fixture
def international_id_v1_empty_doc() -> (
    Document[GeneratedV1Document, Page[GeneratedV1Page]]
):
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR
            / "generated"
            / "response_v1"
            / "empty_international_id_v1.json"
        )
    )

    return Document(GeneratedV1, json_data["document"])


@pytest.fixture
def invoice_v4_empty_doc() -> Document[GeneratedV1Document, Page[GeneratedV1Page]]:
    json_data = json.load(
        open(PRODUCT_DATA_DIR / "generated" / "response_v1" / "empty_invoice_v4.json")
    )
    return Document(GeneratedV1, json_data["document"])


@pytest.fixture
def invoice_v4_complete_doc() -> Document[GeneratedV1Document, Page[GeneratedV1Page]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "generated" / "response_v1" / "complete_invoice_v4.json"
        )
    )
    return Document(GeneratedV1, json_data["document"])


@pytest.fixture
def invoice_v4_page_0() -> Document[GeneratedV1Document, Page[GeneratedV1Page]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "generated" / "response_v1" / "complete_invoice_v4.json"
        )
    )
    return Page(GeneratedV1Page, json_data["document"]["inference"]["pages"][0])


def test_international_id_v1_empty_doc(international_id_v1_empty_doc) -> None:
    doc_str = open(
        PRODUCT_DATA_DIR
        / "generated"
        / "response_v1"
        / "summary_empty_international_id_v1.rst"
    ).read()
    assert str(international_id_v1_empty_doc) == doc_str


def test_international_id_v1_complete_doc(international_id_v1_complete_doc) -> None:
    doc_str = open(
        PRODUCT_DATA_DIR
        / "generated"
        / "response_v1"
        / "summary_full_international_id_v1.rst"
    ).read()
    assert str(international_id_v1_complete_doc) == doc_str


def test_invoice_v4_complete_doc(invoice_v4_complete_doc) -> None:
    doc_str = open(
        PRODUCT_DATA_DIR / "generated" / "response_v1" / "summary_full_invoice_v4.rst"
    ).read()
    assert str(invoice_v4_complete_doc) == doc_str


def test_invoice_v4_page0(invoice_v4_page_0) -> None:
    doc_str = open(
        PRODUCT_DATA_DIR / "generated" / "response_v1" / "summary_page0_invoice_v4.rst"
    ).read()
    assert str(invoice_v4_page_0) == doc_str


def test_invoice_v4_empty_doc(invoice_v4_empty_doc) -> None:
    doc_str = open(
        PRODUCT_DATA_DIR / "generated" / "response_v1" / "summary_empty_invoice_v4.rst"
    ).read()
    assert str(invoice_v4_empty_doc) == doc_str
