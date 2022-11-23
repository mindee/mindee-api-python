import json

import pytest

from mindee.documents import InvoiceV4
from tests import INVOICE_DATA_DIR

FILE_PATH_INVOICE_V4_COMPLETE = f"{INVOICE_DATA_DIR}/response_v4/complete.json"
FILE_PATH_INVOICE_V4_EMPTY = f"{INVOICE_DATA_DIR}/response_v4/empty.json"


@pytest.fixture
def invoice_v4_doc_object():
    json_data = json.load(open(FILE_PATH_INVOICE_V4_COMPLETE))
    return InvoiceV4(api_prediction=json_data["document"]["inference"], page_n=None)


@pytest.fixture
def invoice_v4_doc_object_empty(invoice_pred):
    return InvoiceV4(api_prediction=invoice_pred)


@pytest.fixture
def invoice_v4_page_object():
    json_data = json.load(open(FILE_PATH_INVOICE_V4_COMPLETE))
    return InvoiceV4(
        api_prediction=json_data["document"]["inference"]["pages"][0], page_n=0
    )


@pytest.fixture
def invoice_pred():
    json_data = json.load(open(FILE_PATH_INVOICE_V4_EMPTY))
    return json_data["document"]["inference"]["pages"][0]


def test_doc_constructor(invoice_v4_doc_object):
    assert invoice_v4_doc_object.invoice_date.value == "2020-02-17"
    assert invoice_v4_doc_object.checklist["taxes_match_total_incl"] is True
    assert invoice_v4_doc_object.checklist["taxes_match_total_excl"] is True
    assert (
        invoice_v4_doc_object.checklist["taxes_plus_total_excl_match_total_incl"]
        is True
    )
    assert invoice_v4_doc_object.total_tax.value == 97.98
    assert invoice_v4_doc_object.total_net.value == 489.97
    assert invoice_v4_doc_object.total_amount.value == 587.95
    assert invoice_v4_doc_object.invoice_date.value == "2020-02-17"
    assert invoice_v4_doc_object.invoice_date.confidence == 0.99
    assert invoice_v4_doc_object.invoice_number.value == "0042004801351"
    assert invoice_v4_doc_object.invoice_number.confidence == 0.95
    for line_item in invoice_v4_doc_object.line_items:
        assert line_item.page_n == 0 or line_item.page_n == 1
        assert len(line_item.polygon) == 4
    doc_str = open(f"{INVOICE_DATA_DIR}/response_v4/doc_to_string.txt").read().strip()
    assert str(invoice_v4_doc_object) == doc_str


def test_page_constructor(invoice_v4_page_object):
    doc_str = open(f"{INVOICE_DATA_DIR}/response_v4/page0_to_string.txt").read().strip()
    assert invoice_v4_page_object.orientation.value == 0
    assert invoice_v4_page_object.invoice_number.page_n == 0
    assert str(invoice_v4_page_object) == doc_str
    assert len(invoice_v4_page_object.cropper) == 0
    for line_item in invoice_v4_page_object.line_items:
        assert line_item.page_n == 0
        assert len(line_item.polygon) == 4


def test_all_na(invoice_v4_doc_object_empty):
    assert invoice_v4_doc_object_empty.locale.value is None
    assert invoice_v4_doc_object_empty.total_amount.value is None
    assert invoice_v4_doc_object_empty.total_net.value is None
    assert invoice_v4_doc_object_empty.total_tax.value is None
    assert invoice_v4_doc_object_empty.invoice_date.value is None
    assert invoice_v4_doc_object_empty.invoice_number.value is None
    assert invoice_v4_doc_object_empty.due_date.value is None
    assert len(invoice_v4_doc_object_empty.taxes) == 0
    assert invoice_v4_doc_object_empty.supplier_name.value is None
    assert len(invoice_v4_doc_object_empty.supplier_payment_details) == 0
    assert len(invoice_v4_doc_object_empty.supplier_company_registrations) == 0
    assert invoice_v4_doc_object_empty.orientation is None


def test_checklist_on_empty(invoice_v4_doc_object_empty):
    for check in invoice_v4_doc_object_empty.checklist.values():
        assert check is False


# Business tests
def test__reconstruct_total_amount_from_taxes_plus_excl_1(invoice_pred):
    # no taxes implies no reconstruct for total incl
    invoice_pred["prediction"]["total_amount"] = {"value": "N/A", "confidence": 0.0}
    invoice_pred["prediction"]["total_net"] = {"value": 240.5, "confidence": 0.9}
    invoice_pred["prediction"]["taxes"] = []
    invoice = InvoiceV4(invoice_pred)
    assert invoice.total_amount.value is None


def test__reconstruct_total_amount_from_taxes_plus_excl_2(invoice_pred):
    # no excl implies no reconstruct for total incl
    invoice_pred["prediction"]["total_amount"] = {"value": "N/A", "confidence": 0.0}
    invoice_pred["prediction"]["total_net"] = {"value": "N/A", "confidence": 0.0}
    invoice_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 9.5, "confidence": 0.9}
    ]
    invoice = InvoiceV4(invoice_pred)
    assert invoice.total_amount.value is None


def test__reconstruct_total_amount_from_taxes_plus_excl_3(invoice_pred):
    # incl already exists implies no reconstruct
    invoice_pred["prediction"]["total_amount"] = {"value": 260, "confidence": 0.4}
    invoice_pred["prediction"]["total_net"] = {"value": 240.5, "confidence": 0.9}
    invoice_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 9.5, "confidence": 0.9}
    ]
    invoice = InvoiceV4(invoice_pred)
    assert invoice.total_amount.value == 260
    assert invoice.total_amount.confidence == 0.4


def test__reconstruct_total_amount_from_taxes_plus_excl_4(invoice_pred):
    # working example
    invoice_pred["prediction"]["total_amount"] = {"value": "N/A", "confidence": 0.0}
    invoice_pred["prediction"]["total_net"] = {"value": 240.5, "confidence": 0.9}
    invoice_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 9.5, "confidence": 0.9}
    ]
    invoice = InvoiceV4(invoice_pred)
    assert invoice.total_amount.value == 250
    assert invoice.total_amount.confidence == 0.81


def test__reconstruct_total_net_from_tcc_and_taxes_1(invoice_pred):
    # no incl implies no reconstruct for total excl
    invoice_pred["prediction"]["total_amount"] = {"value": "N/A", "confidence": 0.0}
    invoice_pred["prediction"]["total_net"] = {"value": "N/A", "confidence": 0.0}
    invoice_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 9.5, "confidence": 0.9}
    ]
    invoice = InvoiceV4(invoice_pred)
    assert invoice.total_net.value is None


def test__reconstruct_total_net_from_tcc_and_taxes_2(invoice_pred):
    # no taxes implies no reconstruct for total excl
    invoice_pred["prediction"]["total_amount"] = {"value": 1150.20, "confidence": 0.7}
    invoice_pred["prediction"]["total_net"] = {"value": "N/A", "confidence": 0.0}
    invoice_pred["prediction"]["taxes"] = []
    invoice = InvoiceV4(invoice_pred)
    assert invoice.total_net.value is None


def test__reconstruct_total_net_from_tcc_and_taxes_3(invoice_pred):
    # excl already exists implies no reconstruct
    invoice_pred["prediction"]["total_amount"] = {"value": 1150.20, "confidence": 0.7}
    invoice_pred["prediction"]["total_net"] = {"value": 1050.0, "confidence": 0.4}
    invoice_pred["prediction"]["taxes"] = []
    invoice = InvoiceV4(invoice_pred)
    assert invoice.total_net.value == 1050.0
    assert invoice.total_net.confidence == 0.4


def test__reconstruct_total_net_from_tcc_and_taxes_4(invoice_pred):
    # working example
    invoice_pred["prediction"]["total_amount"] = {"value": 1150.20, "confidence": 0.6}
    invoice_pred["prediction"]["total_net"] = {"value": "N/A", "confidence": 0.0}
    invoice_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 10.2, "confidence": 0.5},
        {"rate": 10, "value": 40.0, "confidence": 0.1},
    ]
    invoice = InvoiceV4(invoice_pred)
    assert invoice.total_net.value == 1100
    assert invoice.total_net.confidence == 0.03


def test__reconstruct_total_tax_1(invoice_pred):
    # no taxes implies no reconstruct for total tax
    invoice_pred["prediction"]["taxes"] = []
    invoice = InvoiceV4(invoice_pred)
    assert invoice.total_tax.value is None


def test__reconstruct_total_tax_2(invoice_pred):
    # working example
    invoice_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 10.2, "confidence": 0.5},
        {"rate": 10, "value": 40.0, "confidence": 0.1},
    ]
    invoice = InvoiceV4(invoice_pred)
    assert invoice.total_tax.value == 50.2
    assert invoice.total_tax.confidence == 0.05


def test__taxes_match_total_amount_1(invoice_pred):
    # matching example
    invoice_pred["prediction"]["total_amount"] = {"value": 507.25, "confidence": 0.6}
    invoice_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 10.99, "confidence": 0.5},
        {"rate": 10, "value": 40.12, "confidence": 0.1},
    ]
    invoice = InvoiceV4(invoice_pred)
    assert invoice.checklist["taxes_match_total_incl"] is True
    assert invoice.total_amount.confidence == 1.0
    for tax in invoice.taxes:
        assert tax.confidence == 1.0


def test__taxes_match_total_amount_2(invoice_pred):
    # not matching example with close error
    invoice_pred["prediction"]["total_amount"] = {"value": 507.25, "confidence": 0.6}
    invoice_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 10.9, "confidence": 0.5},
        {"rate": 10, "value": 40.12, "confidence": 0.1},
    ]
    invoice = InvoiceV4(invoice_pred)
    assert invoice.checklist["taxes_match_total_incl"] is False


def test__taxes_match_total_amount_3(invoice_pred):
    # sanity check with null tax
    invoice_pred["prediction"]["total_amount"] = {"value": 507.25, "confidence": 0.6}
    invoice_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 0.0, "confidence": 0.5}
    ]
    invoice = InvoiceV4(invoice_pred)
    assert invoice.checklist["taxes_match_total_incl"] is False


def test__taxes_match_total_net_1(invoice_pred):
    # matching example
    invoice_pred["prediction"]["total_net"] = {"value": 456.15, "confidence": 0.6}
    invoice_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 10.99, "confidence": 0.5},
        {"rate": 10, "value": 40.12, "confidence": 0.1},
    ]
    invoice = InvoiceV4(invoice_pred)
    assert invoice.checklist["taxes_match_total_excl"] is True
    assert invoice.total_net.confidence == 1.0
    for tax in invoice.taxes:
        assert tax.confidence == 1.0


def test__taxes_match_total_net_2(invoice_pred):
    # not matching example  with close error
    invoice_pred["prediction"]["total_net"] = {"value": 456.15, "confidence": 0.6}
    invoice_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 10.9, "confidence": 0.5},
        {"rate": 10, "value": 40.12, "confidence": 0.1},
    ]
    invoice = InvoiceV4(invoice_pred)
    assert invoice.checklist["taxes_match_total_excl"] is False


def test__taxes_match_total_net_3(invoice_pred):
    # sanity check with null tax
    invoice_pred["prediction"]["total_net"] = {"value": 507.25, "confidence": 0.6}
    invoice_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 0.0, "confidence": 0.5}
    ]
    invoice = InvoiceV4(invoice_pred)
    assert invoice.checklist["taxes_match_total_incl"] is False


def test__taxes_plus_total_net_match_total_amount_1(invoice_pred):
    # matching example
    invoice_pred["prediction"]["total_amount"] = {"value": 507.25, "confidence": 0.6}
    invoice_pred["prediction"]["total_net"] = {"value": 456.15, "confidence": 0.6}
    invoice_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 10.99, "confidence": 0.5},
        {"rate": 10, "value": 40.12, "confidence": 0.1},
    ]
    invoice = InvoiceV4(invoice_pred)
    assert invoice.checklist["taxes_plus_total_excl_match_total_incl"] is True
    assert invoice.total_amount.confidence == 1.0
    assert invoice.total_net.confidence == 1.0
    for tax in invoice.taxes:
        assert tax.confidence == 1.0


def test__taxes_plus_total_net_match_total_amount_2(invoice_pred):
    # not matching example
    invoice_pred["prediction"]["total_amount"] = {"value": 507.2, "confidence": 0.6}
    invoice_pred["prediction"]["total_net"] = {"value": 456.15, "confidence": 0.6}
    invoice_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 10.99, "confidence": 0.5},
        {"rate": 10, "value": 40.12, "confidence": 0.1},
    ]
    invoice = InvoiceV4(invoice_pred)
    assert invoice.checklist["taxes_plus_total_excl_match_total_incl"] is False


def test__taxes_plus_total_net_match_total_amount_3(invoice_pred):
    # sanity check with null tax
    invoice_pred["prediction"]["total_net"] = {"value": 456.15, "confidence": 0.6}
    invoice_pred["prediction"]["total_amount"] = {"value": 507.25, "confidence": 0.6}
    invoice_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 0.0, "confidence": 0.5}
    ]
    invoice = InvoiceV4(invoice_pred)
    assert invoice.checklist["taxes_match_total_incl"] is False


def test__shouldnt_raise_when_tax_rate_none(invoice_pred):
    # sanity check with null tax
    invoice_pred["prediction"]["total_net"] = {"value": 456.15, "confidence": 0.6}
    invoice_pred["prediction"]["total_amount"] = {"value": 507.25, "confidence": 0.6}
    invoice_pred["prediction"]["taxes"] = [
        {"rate": "N/A", "value": 0.0, "confidence": 0.5}
    ]
    invoice = InvoiceV4(invoice_pred)
    assert invoice.checklist["taxes_match_total_incl"] is False


def test_null_tax_rates_dont_raise(invoice_pred):
    invoice_pred["prediction"]["total_net"] = {"value": 12, "confidence": 0.6}
    invoice_pred["prediction"]["total_amount"] = {"value": 15, "confidence": 0.6}
    invoice_pred["prediction"]["taxes"] = [
        {"rate": 1, "value": 0.0, "confidence": 0.5},
        {"rate": 2, "value": 20.0, "confidence": 0.5},
    ]
    invoice = InvoiceV4(invoice_pred)
    assert invoice.checklist["taxes_match_total_incl"] is False
    assert invoice.checklist["taxes_match_total_excl"] is False
