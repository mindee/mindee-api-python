import json

import pytest

from mindee.documents.invoice.invoice_v3 import InvoiceV3
from tests import INVOICE_DATA_DIR

INVOICE_FILE_PATH = f"{INVOICE_DATA_DIR}/response_v3/complete.json"
INVOICE_NA_FILE_PATH = f"{INVOICE_DATA_DIR}/response_v3/empty.json"


@pytest.fixture
def invoice_object():
    json_data = json.load(open(INVOICE_FILE_PATH))
    return InvoiceV3(json_data["document"]["inference"]["prediction"], page_n=None)


@pytest.fixture
def invoice_object_all_na(invoice_pred):
    return InvoiceV3(invoice_pred)


@pytest.fixture
def invoice_pred():
    json_data = json.load(open(INVOICE_NA_FILE_PATH))
    return json_data["document"]["inference"]["pages"][0]["prediction"]


# Technical tests
def test_constructor(invoice_object):
    assert invoice_object.invoice_date.value == "2020-02-17"
    assert invoice_object.checklist["taxes_match_total_incl"] is True
    assert invoice_object.checklist["taxes_match_total_excl"] is True
    assert invoice_object.checklist["taxes_plus_total_excl_match_total_incl"] is True
    assert invoice_object.total_tax.value == 97.98
    assert invoice_object.invoice_date.value == "2020-02-17"
    assert invoice_object.invoice_date.confidence == 0.99
    assert invoice_object.invoice_number.value == "0042004801351"
    assert invoice_object.invoice_number.confidence == 0.95
    doc_str = open(f"{INVOICE_DATA_DIR}/response_v3/doc_to_string.txt").read().strip()
    assert str(invoice_object) == doc_str


def test_all_na(invoice_object_all_na):
    assert invoice_object_all_na.locale.value is None
    assert invoice_object_all_na.total_incl.value is None
    assert invoice_object_all_na.total_excl.value is None
    assert invoice_object_all_na.total_tax.value is None
    assert invoice_object_all_na.invoice_date.value is None
    assert invoice_object_all_na.invoice_number.value is None
    assert invoice_object_all_na.due_date.value is None
    assert len(invoice_object_all_na.taxes) == 0
    assert invoice_object_all_na.supplier.value is None
    assert len(invoice_object_all_na.payment_details) == 0
    assert len(invoice_object_all_na.company_number) == 0
    assert invoice_object_all_na.orientation is None


def test_checklist_on_empty(invoice_object_all_na):
    for check in invoice_object_all_na.checklist.values():
        assert check is False


# Business tests
def test__reconstruct_total_incl_from_taxes_plus_excl_1(invoice_pred):
    # no taxes implies no reconstruct for total incl
    invoice_pred["total_incl"] = {"value": "N/A", "confidence": 0.0}
    invoice_pred["total_excl"] = {"value": 240.5, "confidence": 0.9}
    invoice_pred["taxes"] = []
    invoice = InvoiceV3(invoice_pred)
    assert invoice.total_incl.value is None


def test__reconstruct_total_incl_from_taxes_plus_excl_2(invoice_pred):
    # no excl implies no reconstruct for total incl
    invoice_pred["total_incl"] = {"value": "N/A", "confidence": 0.0}
    invoice_pred["total_excl"] = {"value": "N/A", "confidence": 0.0}
    invoice_pred["taxes"] = [{"rate": 20, "value": 9.5, "confidence": 0.9}]
    invoice = InvoiceV3(invoice_pred)
    assert invoice.total_incl.value is None


def test__reconstruct_total_incl_from_taxes_plus_excl_3(invoice_pred):
    # incl already exists implies no reconstruct
    invoice_pred["total_incl"] = {"value": 260, "confidence": 0.4}
    invoice_pred["total_excl"] = {"value": 240.5, "confidence": 0.9}
    invoice_pred["taxes"] = [{"rate": 20, "value": 9.5, "confidence": 0.9}]
    invoice = InvoiceV3(invoice_pred)
    assert invoice.total_incl.value == 260
    assert invoice.total_incl.confidence == 0.4


def test__reconstruct_total_incl_from_taxes_plus_excl_4(invoice_pred):
    # working example
    invoice_pred["total_incl"] = {"value": "N/A", "confidence": 0.0}
    invoice_pred["total_excl"] = {"value": 240.5, "confidence": 0.9}
    invoice_pred["taxes"] = [{"rate": 20, "value": 9.5, "confidence": 0.9}]
    invoice = InvoiceV3(invoice_pred)
    assert invoice.total_incl.value == 250
    assert invoice.total_incl.confidence == 0.81


def test__reconstruct_total_excl_from_tcc_and_taxes_1(invoice_pred):
    # no incl implies no reconstruct for total excl
    invoice_pred["total_incl"] = {"value": "N/A", "confidence": 0.0}
    invoice_pred["total_excl"] = {"value": "N/A", "confidence": 0.0}
    invoice_pred["taxes"] = [{"rate": 20, "value": 9.5, "confidence": 0.9}]
    invoice = InvoiceV3(invoice_pred)
    assert invoice.total_excl.value is None


def test__reconstruct_total_excl_from_tcc_and_taxes_2(invoice_pred):
    # no taxes implies no reconstruct for total excl
    invoice_pred["total_incl"] = {"value": 1150.20, "confidence": 0.7}
    invoice_pred["total_excl"] = {"value": "N/A", "confidence": 0.0}
    invoice_pred["taxes"] = []
    invoice = InvoiceV3(invoice_pred)
    assert invoice.total_excl.value is None


def test__reconstruct_total_excl_from_tcc_and_taxes_3(invoice_pred):
    # excl already exists implies no reconstruct
    invoice_pred["total_incl"] = {"value": 1150.20, "confidence": 0.7}
    invoice_pred["total_excl"] = {"value": 1050.0, "confidence": 0.4}
    invoice_pred["taxes"] = []
    invoice = InvoiceV3(invoice_pred)
    assert invoice.total_excl.value == 1050.0
    assert invoice.total_excl.confidence == 0.4


def test__reconstruct_total_excl_from_tcc_and_taxes_4(invoice_pred):
    # working example
    invoice_pred["total_incl"] = {"value": 1150.20, "confidence": 0.6}
    invoice_pred["total_excl"] = {"value": "N/A", "confidence": 0.0}
    invoice_pred["taxes"] = [
        {"rate": 20, "value": 10.2, "confidence": 0.5},
        {"rate": 10, "value": 40.0, "confidence": 0.1},
    ]
    invoice = InvoiceV3(invoice_pred)
    assert invoice.total_excl.value == 1100
    assert invoice.total_excl.confidence == 0.03


def test__reconstruct_total_tax_1(invoice_pred):
    # no taxes implies no reconstruct for total tax
    invoice_pred["taxes"] = []
    invoice = InvoiceV3(invoice_pred)
    assert invoice.total_tax.value is None


def test__reconstruct_total_tax_2(invoice_pred):
    # working example
    invoice_pred["taxes"] = [
        {"rate": 20, "value": 10.2, "confidence": 0.5},
        {"rate": 10, "value": 40.0, "confidence": 0.1},
    ]
    invoice = InvoiceV3(invoice_pred)
    assert invoice.total_tax.value == 50.2
    assert invoice.total_tax.confidence == 0.05


def test__taxes_match_total_incl_1(invoice_pred):
    # matching example
    invoice_pred["total_incl"] = {"value": 507.25, "confidence": 0.6}
    invoice_pred["taxes"] = [
        {"rate": 20, "value": 10.99, "confidence": 0.5},
        {"rate": 10, "value": 40.12, "confidence": 0.1},
    ]
    invoice = InvoiceV3(invoice_pred)
    assert invoice.checklist["taxes_match_total_incl"] is True
    assert invoice.total_incl.confidence == 1.0
    for tax in invoice.taxes:
        assert tax.confidence == 1.0


def test__taxes_match_total_incl_2(invoice_pred):
    # not matching example with close error
    invoice_pred["total_incl"] = {"value": 507.25, "confidence": 0.6}
    invoice_pred["taxes"] = [
        {"rate": 20, "value": 10.9, "confidence": 0.5},
        {"rate": 10, "value": 40.12, "confidence": 0.1},
    ]
    invoice = InvoiceV3(invoice_pred)
    assert invoice.checklist["taxes_match_total_incl"] is False


def test__taxes_match_total_incl_3(invoice_pred):
    # sanity check with null tax
    invoice_pred["total_incl"] = {"value": 507.25, "confidence": 0.6}
    invoice_pred["taxes"] = [{"rate": 20, "value": 0.0, "confidence": 0.5}]
    invoice = InvoiceV3(invoice_pred)
    assert invoice.checklist["taxes_match_total_incl"] is False


def test__taxes_match_total_excl_1(invoice_pred):
    # matching example
    invoice_pred["total_excl"] = {"value": 456.15, "confidence": 0.6}
    invoice_pred["taxes"] = [
        {"rate": 20, "value": 10.99, "confidence": 0.5},
        {"rate": 10, "value": 40.12, "confidence": 0.1},
    ]
    invoice = InvoiceV3(invoice_pred)
    assert invoice.checklist["taxes_match_total_excl"] is True
    assert invoice.total_excl.confidence == 1.0
    for tax in invoice.taxes:
        assert tax.confidence == 1.0


def test__taxes_match_total_excl_2(invoice_pred):
    # not matching example  with close error
    invoice_pred["total_excl"] = {"value": 456.15, "confidence": 0.6}
    invoice_pred["taxes"] = [
        {"rate": 20, "value": 10.9, "confidence": 0.5},
        {"rate": 10, "value": 40.12, "confidence": 0.1},
    ]
    invoice = InvoiceV3(invoice_pred)
    assert invoice.checklist["taxes_match_total_excl"] is False


def test__taxes_match_total_excl_3(invoice_pred):
    # sanity check with null tax
    invoice_pred["total_excl"] = {"value": 507.25, "confidence": 0.6}
    invoice_pred["taxes"] = [{"rate": 20, "value": 0.0, "confidence": 0.5}]
    invoice = InvoiceV3(invoice_pred)
    assert invoice.checklist["taxes_match_total_incl"] is False


def test__taxes_plus_total_excl_match_total_incl_1(invoice_pred):
    # matching example
    invoice_pred["total_incl"] = {"value": 507.25, "confidence": 0.6}
    invoice_pred["total_excl"] = {"value": 456.15, "confidence": 0.6}
    invoice_pred["taxes"] = [
        {"rate": 20, "value": 10.99, "confidence": 0.5},
        {"rate": 10, "value": 40.12, "confidence": 0.1},
    ]
    invoice = InvoiceV3(invoice_pred)
    assert invoice.checklist["taxes_plus_total_excl_match_total_incl"] is True
    assert invoice.total_incl.confidence == 1.0
    assert invoice.total_excl.confidence == 1.0
    for tax in invoice.taxes:
        assert tax.confidence == 1.0


def test__taxes_plus_total_excl_match_total_incl_2(invoice_pred):
    # not matching example
    invoice_pred["total_incl"] = {"value": 507.2, "confidence": 0.6}
    invoice_pred["total_excl"] = {"value": 456.15, "confidence": 0.6}
    invoice_pred["taxes"] = [
        {"rate": 20, "value": 10.99, "confidence": 0.5},
        {"rate": 10, "value": 40.12, "confidence": 0.1},
    ]
    invoice = InvoiceV3(invoice_pred)
    assert invoice.checklist["taxes_plus_total_excl_match_total_incl"] is False


def test__taxes_plus_total_excl_match_total_incl_3(invoice_pred):
    # sanity check with null tax
    invoice_pred["total_excl"] = {"value": 456.15, "confidence": 0.6}
    invoice_pred["total_incl"] = {"value": 507.25, "confidence": 0.6}
    invoice_pred["taxes"] = [{"rate": 20, "value": 0.0, "confidence": 0.5}]
    invoice = InvoiceV3(invoice_pred)
    assert invoice.checklist["taxes_match_total_incl"] is False


def test__shouldnt_raise_when_tax_rate_none(invoice_pred):
    # sanity check with null tax
    invoice_pred["total_excl"] = {"value": 456.15, "confidence": 0.6}
    invoice_pred["total_incl"] = {"value": 507.25, "confidence": 0.6}
    invoice_pred["taxes"] = [{"rate": "N/A", "value": 0.0, "confidence": 0.5}]
    invoice = InvoiceV3(invoice_pred)
    assert invoice.checklist["taxes_match_total_incl"] is False


def test_null_tax_rates_dont_raise(invoice_pred):
    invoice_pred["total_excl"] = {"value": 12, "confidence": 0.6}
    invoice_pred["total_incl"] = {"value": 15, "confidence": 0.6}
    invoice_pred["taxes"] = [
        {"rate": 1, "value": 0.0, "confidence": 0.5},
        {"rate": 2, "value": 20.0, "confidence": 0.5},
    ]
    invoice = InvoiceV3(invoice_pred)
    assert invoice.checklist["taxes_match_total_incl"] is False
    assert invoice.checklist["taxes_match_total_excl"] is False
