import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.invoice.invoice_v4 import InvoiceV4
from mindee.product.invoice.invoice_v4_document import (
    InvoiceV4Document,
)
from tests.product import PRODUCT_DATA_DIR

RESPONSE_DIR = PRODUCT_DATA_DIR / "invoices" / "response_v4"

InvoiceV4DocumentType = Document[
    InvoiceV4Document,
    Page[InvoiceV4Document],
]


@pytest.fixture
def complete_doc() -> InvoiceV4DocumentType:
    file_path = RESPONSE_DIR / "complete.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(InvoiceV4, json_data["document"])


@pytest.fixture
def empty_doc() -> InvoiceV4DocumentType:
    file_path = RESPONSE_DIR / "empty.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(InvoiceV4, json_data["document"])


def test_complete_doc(complete_doc: InvoiceV4DocumentType):
    file_path = RESPONSE_DIR / "summary_full.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: InvoiceV4DocumentType):
    prediction = empty_doc.inference.prediction
    assert prediction.locale.value is None
    assert prediction.invoice_number.value is None
    assert prediction.po_number.value is None
    assert len(prediction.reference_numbers) == 0
    assert prediction.date.value is None
    assert prediction.due_date.value is None
    assert prediction.payment_date.value is None
    assert prediction.total_net.value is None
    assert prediction.total_amount.value is None
    assert prediction.total_tax.value is None
    assert len(prediction.taxes) == 0
    assert len(prediction.supplier_payment_details) == 0
    assert prediction.supplier_name.value is None
    assert len(prediction.supplier_company_registrations) == 0
    assert prediction.supplier_address.value is None
    assert prediction.supplier_phone_number.value is None
    assert prediction.supplier_website.value is None
    assert prediction.supplier_email.value is None
    assert prediction.customer_name.value is None
    assert len(prediction.customer_company_registrations) == 0
    assert prediction.customer_address.value is None
    assert prediction.customer_id.value is None
    assert prediction.shipping_address.value is None
    assert prediction.billing_address.value is None
    assert len(prediction.line_items) == 0
