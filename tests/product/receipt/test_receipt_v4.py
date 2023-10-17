import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.receipt.receipt_v4 import ReceiptV4
from mindee.product.receipt.receipt_v4_document import ReceiptV4Document
from tests.product import PRODUCT_DATA_DIR


@pytest.fixture
def complete_doc() -> Document[ReceiptV4Document, Page[ReceiptV4Document]]:
    json_data = json.load(
        open(PRODUCT_DATA_DIR / "expense_receipts" / "response_v4" / "complete.json")
    )
    return Document(ReceiptV4, json_data["document"])


@pytest.fixture
def empty_doc() -> Document[ReceiptV4Document, Page[ReceiptV4Document]]:
    json_data = json.load(
        open(PRODUCT_DATA_DIR / "expense_receipts" / "response_v4" / "empty.json")
    )
    return Document(ReceiptV4, json_data["document"])


@pytest.fixture
def complete_page_0() -> Page[ReceiptV4Document]:
    json_data = json.load(
        open(PRODUCT_DATA_DIR / "expense_receipts" / "response_v4" / "complete.json")
    )
    return Page(ReceiptV4Document, json_data["document"]["inference"]["pages"][0])


def test_complete_doc(
    complete_doc: Document[ReceiptV4Document, Page[ReceiptV4Document]]
):
    reference_str = open(
        PRODUCT_DATA_DIR / "expense_receipts" / "response_v4" / "summary_full.rst",
        "r",
        encoding="utf-8",
    ).read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: Document[ReceiptV4Document, Page[ReceiptV4Document]]):
    prediction = empty_doc.inference.prediction
    assert prediction.locale.value is None
    assert prediction.date.value is None
    assert prediction.time.value is None
    assert prediction.total_amount.value is None
    assert prediction.total_net.value is None
    assert prediction.total_tax.value is None
    assert prediction.tip.value is None
    assert len(prediction.taxes) == 0
    assert prediction.supplier.value is None


def test_complete_page_0(complete_page_0: Page[ReceiptV4Document]):
    reference_str = open(
        PRODUCT_DATA_DIR / "expense_receipts" / "response_v4" / "summary_page0.rst",
        "r",
        encoding="utf-8",
    ).read()
    assert complete_page_0.orientation
    assert complete_page_0.orientation.value == 0
    assert complete_page_0.id == 0
    assert str(complete_page_0) == reference_str
