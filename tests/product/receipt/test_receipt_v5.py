import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.receipt.receipt_v5 import ReceiptV5
from mindee.product.receipt.receipt_v5_document import (
    ReceiptV5Document,
)
from tests.product import PRODUCT_DATA_DIR

RESPONSE_DIR = PRODUCT_DATA_DIR / "expense_receipts" / "response_v5"

ReceiptV5DocumentType = Document[
    ReceiptV5Document,
    Page[ReceiptV5Document],
]


@pytest.fixture
def complete_doc() -> ReceiptV5DocumentType:
    file_path = RESPONSE_DIR / "complete.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(ReceiptV5, json_data["document"])


@pytest.fixture
def empty_doc() -> ReceiptV5DocumentType:
    file_path = RESPONSE_DIR / "empty.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(ReceiptV5, json_data["document"])


def test_complete_doc(complete_doc: ReceiptV5DocumentType):
    file_path = RESPONSE_DIR / "summary_full.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: ReceiptV5DocumentType):
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
    assert prediction.receipt_number.value is None
    assert len(prediction.line_items) == 0
