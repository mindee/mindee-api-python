import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product import InvoiceV4
from mindee.product.invoice.invoice_v4_document import InvoiceV4Document
from tests.product import PRODUCT_DATA_DIR


@pytest.fixture
def complete_doc() -> Document[InvoiceV4Document, Page[InvoiceV4Document]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "invoices" / "response_v4" / "complete.json",
            encoding="utf-8",
        )
    )
    return Document(InvoiceV4, json_data["document"])


@pytest.fixture
def empty_doc() -> Document[InvoiceV4Document, Page[InvoiceV4Document]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "invoices" / "response_v4" / "empty.json",
            encoding="utf-8",
        )
    )
    return Document(InvoiceV4, json_data["document"])


@pytest.fixture
def complete_page_0() -> Page[InvoiceV4Document]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "invoices" / "response_v4" / "complete.json",
            encoding="utf-8",
        )
    )
    return Page(InvoiceV4Document, json_data["document"]["inference"]["pages"][0])


def test_complete_doc(
    complete_doc: Document[InvoiceV4Document, Page[InvoiceV4Document]]
):
    reference_str = open(
        PRODUCT_DATA_DIR / "invoices" / "response_v4" / "summary_full.rst",
        "r",
        encoding="utf-8",
    ).read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: Document[InvoiceV4Document, Page[InvoiceV4Document]]):
    prediction = empty_doc.inference.prediction
    assert prediction.locale.value is None
    assert prediction.invoice_number.value is None
    assert len(prediction.reference_numbers) == 0
    assert prediction.date.value is None
    assert prediction.due_date.value is None
    assert prediction.total_net.value is None
    assert prediction.total_amount.value is None
    assert prediction.total_tax.value is None
    assert len(prediction.taxes) == 0
    assert len(prediction.supplier_payment_details) == 0
    assert prediction.supplier_name.value is None
    assert len(prediction.supplier_company_registrations) == 0
    assert prediction.supplier_address.value is None
    assert prediction.customer_name.value is None
    assert len(prediction.customer_company_registrations) == 0
    assert prediction.customer_address.value is None
    assert prediction.shipping_address.value is None
    assert prediction.billing_address.value is None
    assert len(prediction.line_items) == 0
