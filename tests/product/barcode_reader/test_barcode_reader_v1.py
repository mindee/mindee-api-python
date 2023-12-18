import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product import BarcodeReaderV1
from mindee.product.barcode_reader.barcode_reader_v1_document import (
    BarcodeReaderV1Document,
)
from tests.product import PRODUCT_DATA_DIR


@pytest.fixture
def complete_doc() -> Document[BarcodeReaderV1Document, Page[BarcodeReaderV1Document]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "barcode_reader" / "response_v1" / "complete.json",
            encoding="utf-8",
        )
    )
    return Document(BarcodeReaderV1, json_data["document"])


@pytest.fixture
def empty_doc() -> Document[BarcodeReaderV1Document, Page[BarcodeReaderV1Document]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "barcode_reader" / "response_v1" / "empty.json",
            encoding="utf-8",
        )
    )
    return Document(BarcodeReaderV1, json_data["document"])


@pytest.fixture
def complete_page_0() -> Page[BarcodeReaderV1Document]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "barcode_reader" / "response_v1" / "complete.json",
            encoding="utf-8",
        )
    )
    return Page(BarcodeReaderV1Document, json_data["document"]["inference"]["pages"][0])


def test_complete_doc(
    complete_doc: Document[BarcodeReaderV1Document, Page[BarcodeReaderV1Document]]
):
    reference_str = open(
        PRODUCT_DATA_DIR / "barcode_reader" / "response_v1" / "summary_full.rst",
        "r",
        encoding="utf-8",
    ).read()
    assert str(complete_doc) == reference_str


def test_empty_doc(
    empty_doc: Document[BarcodeReaderV1Document, Page[BarcodeReaderV1Document]]
):
    prediction = empty_doc.inference.prediction
    assert len(prediction.codes_1d) == 0
    assert len(prediction.codes_2d) == 0
