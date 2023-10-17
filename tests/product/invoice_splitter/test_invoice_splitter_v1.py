import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.invoice_splitter.invoice_splitter_v1 import InvoiceSplitterV1
from mindee.product.invoice_splitter.invoice_splitter_v1_document import (
    InvoiceSplitterV1Document,
)
from tests.product import PRODUCT_DATA_DIR


@pytest.fixture
def complete_doc() -> (
    Document[InvoiceSplitterV1Document, Page[InvoiceSplitterV1Document]]
):
    json_data = json.load(
        open(PRODUCT_DATA_DIR / "invoice_splitter" / "response_v1" / "complete.json")
    )
    return Document(InvoiceSplitterV1, json_data["document"])


@pytest.fixture
def empty_doc() -> Document[InvoiceSplitterV1Document, Page[InvoiceSplitterV1Document]]:
    json_data = json.load(
        open(PRODUCT_DATA_DIR / "invoice_splitter" / "response_v1" / "empty.json")
    )
    return Document(InvoiceSplitterV1, json_data["document"])


def test_complete_doc(
    complete_doc: Document[InvoiceSplitterV1Document, Page[InvoiceSplitterV1Document]],
):
    reference_str = open(
        PRODUCT_DATA_DIR / "invoice_splitter" / "response_v1" / "summary_full.rst",
        "r",
        encoding="utf-8",
    ).read()
    assert len(complete_doc.inference.prediction.invoice_page_groups) == 3
    assert complete_doc.inference.prediction.invoice_page_groups[0].confidence == 1
    assert complete_doc.inference.prediction.invoice_page_groups[2].confidence == 0
    assert str(complete_doc) == reference_str


def test_empty_doc(
    empty_doc: Document[InvoiceSplitterV1Document, Page[InvoiceSplitterV1Document]]
):
    assert len(empty_doc.inference.prediction.invoice_page_groups) == 0
