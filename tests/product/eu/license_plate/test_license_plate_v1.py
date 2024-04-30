import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.eu import LicensePlateV1
from mindee.product.eu.license_plate.license_plate_v1_document import (
    LicensePlateV1Document,
)
from tests.product import PRODUCT_DATA_DIR

RESPONSE_DIR = PRODUCT_DATA_DIR / "license_plates" / "response_v1"

LicensePlateV1DocumentType = Document[
    LicensePlateV1Document,
    Page[LicensePlateV1Document],
]


@pytest.fixture
def complete_doc() -> LicensePlateV1DocumentType:
    file_path = RESPONSE_DIR / "complete.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(LicensePlateV1, json_data["document"])


@pytest.fixture
def empty_doc() -> LicensePlateV1DocumentType:
    file_path = RESPONSE_DIR / "empty.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(LicensePlateV1, json_data["document"])


def test_complete_doc(complete_doc: LicensePlateV1DocumentType):
    file_path = RESPONSE_DIR / "summary_full.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: LicensePlateV1DocumentType):
    prediction = empty_doc.inference.prediction
    assert len(prediction.license_plates) == 0
