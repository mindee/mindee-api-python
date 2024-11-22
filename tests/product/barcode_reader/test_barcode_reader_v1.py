import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.barcode_reader.barcode_reader_v1 import BarcodeReaderV1
from mindee.product.barcode_reader.barcode_reader_v1_document import (
    BarcodeReaderV1Document,
)
from tests.product import PRODUCT_DATA_DIR

RESPONSE_DIR = PRODUCT_DATA_DIR / "barcode_reader" / "response_v1"

BarcodeReaderV1DocumentType = Document[
    BarcodeReaderV1Document,
    Page[BarcodeReaderV1Document],
]


@pytest.fixture
def complete_doc() -> BarcodeReaderV1DocumentType:
    file_path = RESPONSE_DIR / "complete.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(BarcodeReaderV1, json_data["document"])


@pytest.fixture
def empty_doc() -> BarcodeReaderV1DocumentType:
    file_path = RESPONSE_DIR / "empty.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(BarcodeReaderV1, json_data["document"])


def test_complete_doc(complete_doc: BarcodeReaderV1DocumentType):
    file_path = RESPONSE_DIR / "summary_full.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: BarcodeReaderV1DocumentType):
    prediction = empty_doc.inference.prediction
    assert len(prediction.codes_1d) == 0
    assert len(prediction.codes_2d) == 0
