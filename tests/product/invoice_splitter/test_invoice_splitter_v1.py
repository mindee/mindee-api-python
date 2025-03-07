import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.invoice_splitter.invoice_splitter_v1 import InvoiceSplitterV1
from mindee.product.invoice_splitter.invoice_splitter_v1_document import (
    InvoiceSplitterV1Document,
)
from tests.product import PRODUCT_DATA_DIR

RESPONSE_DIR = PRODUCT_DATA_DIR / "invoice_splitter" / "response_v1"

InvoiceSplitterV1DocumentType = Document[
    InvoiceSplitterV1Document,
    Page[InvoiceSplitterV1Document],
]


@pytest.fixture
def complete_doc() -> InvoiceSplitterV1DocumentType:
    file_path = RESPONSE_DIR / "complete.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(InvoiceSplitterV1, json_data["document"])


@pytest.fixture
def empty_doc() -> InvoiceSplitterV1DocumentType:
    file_path = RESPONSE_DIR / "empty.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(InvoiceSplitterV1, json_data["document"])


def test_complete_doc(complete_doc: InvoiceSplitterV1DocumentType):
    file_path = RESPONSE_DIR / "summary_full.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: InvoiceSplitterV1DocumentType):
    prediction = empty_doc.inference.prediction
    assert len(prediction.invoice_page_groups) == 0
