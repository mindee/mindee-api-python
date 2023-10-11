import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.eu import LicensePlateV1
from mindee.product.eu.license_plate.license_plate_v1_document import (
    LicensePlateV1Document,
)
from tests.product import PRODUCT_DATA_DIR


@pytest.fixture
def complete_doc() -> Document[LicensePlateV1Document, Page[LicensePlateV1Document]]:
    json_data = json.load(
        open(PRODUCT_DATA_DIR / "license_plates" / "response_v1" / "complete.json")
    )
    return Document(LicensePlateV1, json_data["document"])


@pytest.fixture
def empty_doc() -> Document[LicensePlateV1Document, Page[LicensePlateV1Document]]:
    json_data = json.load(
        open(PRODUCT_DATA_DIR / "license_plates" / "response_v1" / "empty.json")
    )
    return Document(LicensePlateV1, json_data["document"])


@pytest.fixture
def complete_page_0() -> Page[LicensePlateV1Document]:
    json_data = json.load(
        open(PRODUCT_DATA_DIR / "license_plates" / "response_v1" / "complete.json")
    )
    return Page(LicensePlateV1Document, json_data["document"]["inference"]["pages"][0])


def test_complete_doc(
    complete_doc: Document[LicensePlateV1Document, Page[LicensePlateV1Document]]
):
    reference_str = open(
        PRODUCT_DATA_DIR / "license_plates" / "response_v1" / "summary_full.rst",
        "r",
        encoding="utf-8",
    ).read()
    assert str(complete_doc) == reference_str


def test_empty_doc(
    empty_doc: Document[LicensePlateV1Document, Page[LicensePlateV1Document]]
):
    prediction = empty_doc.inference.prediction
    assert len(prediction.license_plates) == 0


def test_complete_page_0(complete_page_0: Page[LicensePlateV1Document]):
    reference_str = open(
        PRODUCT_DATA_DIR / "license_plates" / "response_v1" / "summary_page0.rst",
        "r",
        encoding="utf-8",
    ).read()
    assert complete_page_0.id == 0
    assert str(complete_page_0) == reference_str
