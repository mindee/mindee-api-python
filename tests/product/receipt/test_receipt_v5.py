import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product import ReceiptV5
from mindee.product.receipt.receipt_v5_document import ReceiptV5Document
from tests.product import PRODUCT_DATA_DIR


@pytest.fixture
def complete_doc() -> Document[ReceiptV5Document, Page[ReceiptV5Document]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "expense_receipts" / "response_v5" / "complete.json",
            encoding="utf-8",
        )
    )
    return Document(ReceiptV5, json_data["document"])


@pytest.fixture
def empty_doc() -> Document[ReceiptV5Document, Page[ReceiptV5Document]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "expense_receipts" / "response_v5" / "empty.json",
            encoding="utf-8",
        )
    )
    return Document(ReceiptV5, json_data["document"])


@pytest.fixture
def complete_page_0() -> Page[ReceiptV5Document]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "expense_receipts" / "response_v5" / "complete.json",
            encoding="utf-8",
        )
    )
    return Page(ReceiptV5Document, json_data["document"]["inference"]["pages"][0])


def test_complete_doc(
    complete_doc: Document[ReceiptV5Document, Page[ReceiptV5Document]]
):
    reference_str = open(
        PRODUCT_DATA_DIR / "expense_receipts" / "response_v5" / "summary_full.rst",
        "r",
        encoding="utf-8",
    ).read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: Document[ReceiptV5Document, Page[ReceiptV5Document]]):
    prediction = empty_doc.inference.prediction
    assert prediction.locale.value is None
    assert prediction.date.value is None
    assert prediction.time.value is None
    assert prediction.total_amount.value is None
    assert prediction.total_net.value is None
    assert prediction.total_tax.value is None
    assert prediction.tip.value is None
    assert len(prediction.taxes) == 0
    assert prediction.supplier_name.value is None
    assert len(prediction.supplier_company_registrations) == 0
    assert prediction.supplier_address.value is None
    assert prediction.supplier_phone_number.value is None
    assert len(prediction.line_items) == 0
