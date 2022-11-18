import json

import pytest

from mindee.documents.financial.financial_v1 import FinancialV1
from tests.documents.test_invoice_v3 import (
    FILE_PATH_INVOICE_V3_COMPLETE,
    FILE_PATH_INVOICE_V3_EMPTY,
)
from tests.documents.test_receipt_v3 import (
    FILE_PATH_RECEIPT_V3_COMPLETE,
    FILE_PATH_RECEIPT_V3_EMPTY,
)


@pytest.fixture
def financial_doc_from_invoice_object():
    json_data = json.load(open(FILE_PATH_INVOICE_V3_COMPLETE))
    return FinancialV1(api_prediction=json_data["document"]["inference"], page_n=None)


@pytest.fixture
def financial_doc_from_receipt_object():
    json_data = json.load(open(FILE_PATH_RECEIPT_V3_COMPLETE))
    return FinancialV1(api_prediction=json_data["document"]["inference"], page_n=None)


@pytest.fixture
def financial_doc_from_receipt_object_all_na():
    json_data = json.load(open(FILE_PATH_RECEIPT_V3_EMPTY))
    return FinancialV1(api_prediction=json_data["document"]["inference"]["pages"][0])


@pytest.fixture
def financial_doc_from_invoice_object_all_na():
    json_data = json.load(open(FILE_PATH_INVOICE_V3_EMPTY))
    return FinancialV1(api_prediction=json_data["document"]["inference"]["pages"][0])


@pytest.fixture
def receipt_pred():
    return json.load(open(FILE_PATH_RECEIPT_V3_EMPTY))["document"]["inference"][
        "pages"
    ][0]


@pytest.fixture
def invoice_pred():
    return json.load(open(FILE_PATH_INVOICE_V3_EMPTY))["document"]["inference"][
        "pages"
    ][0]


def test_constructor_1(financial_doc_from_invoice_object):
    assert financial_doc_from_invoice_object.date.value == "2020-02-17"
    assert (
        financial_doc_from_invoice_object.supplier_address.value
        == "156 University Ave, Toronto ON, Canada M5H 2H7"
    )


def test_constructor_2(financial_doc_from_receipt_object):
    assert financial_doc_from_receipt_object.date.value == "2016-02-26"
    assert financial_doc_from_receipt_object.supplier_address.value is None


def test_all_na_receipt(financial_doc_from_receipt_object_all_na):
    assert financial_doc_from_receipt_object_all_na.orientation is None
    assert financial_doc_from_receipt_object_all_na.locale.value is None
    assert financial_doc_from_receipt_object_all_na.total_incl.value is None
    assert financial_doc_from_receipt_object_all_na.date.value is None
    assert financial_doc_from_receipt_object_all_na.merchant_name.value is None
    assert financial_doc_from_receipt_object_all_na.total_tax.value is None
    assert len(financial_doc_from_receipt_object_all_na.taxes) == 0


def test_all_na_invoice(financial_doc_from_invoice_object_all_na):
    assert financial_doc_from_invoice_object_all_na.orientation is None
    assert financial_doc_from_invoice_object_all_na.locale.value is None
    assert financial_doc_from_invoice_object_all_na.total_incl.value is None
    assert financial_doc_from_invoice_object_all_na.date.value is None
    assert financial_doc_from_invoice_object_all_na.merchant_name.value is None
    assert financial_doc_from_invoice_object_all_na.total_tax.value is None
    assert len(financial_doc_from_invoice_object_all_na.taxes) == 0


def test__str__invoice(financial_doc_from_invoice_object):
    assert type(financial_doc_from_invoice_object.__str__()) == str


def test__str__receipt(financial_doc_from_receipt_object):
    assert type(financial_doc_from_receipt_object.__str__()) == str


# Business tests from receipt
def test__receipt_reconstruct_total_excl_from_total_and_taxes_1(receipt_pred):
    # no incl implies no reconstruct for total excl
    receipt_pred["prediction"]["total_incl"] = {"value": "N/A", "confidence": 0.0}
    receipt_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 9.5, "confidence": 0.9}
    ]
    financial_doc = FinancialV1(receipt_pred)
    assert financial_doc.total_excl.value is None


def test__receipt_reconstruct_total_excl_from_total_and_taxes_2(receipt_pred):
    # no taxes implies no reconstruct for total excl
    receipt_pred["prediction"]["total_incl"] = {"value": 12.54, "confidence": 0.0}
    receipt_pred["prediction"]["taxes"] = []
    financial_doc = FinancialV1(receipt_pred)
    assert financial_doc.total_excl.value is None


def test__receipt_reconstruct_total_excl_from_total_and_taxes_3(receipt_pred):
    # working example
    receipt_pred["prediction"]["total_incl"] = {"value": 12.54, "confidence": 0.5}
    receipt_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 0.5, "confidence": 0.1},
        {"rate": 10, "value": 4.25, "confidence": 0.6},
    ]
    financial_doc = FinancialV1(receipt_pred)
    assert financial_doc.total_excl.confidence == 0.03
    assert financial_doc.total_excl.value == 7.79


def test__receipt_reconstruct_total_tax_1(receipt_pred):
    # no taxes implies no reconstruct for total tax
    receipt_pred["prediction"]["taxes"] = []
    financial_doc = FinancialV1(receipt_pred)
    assert financial_doc.total_tax.value is None


def test__receipt_reconstruct_total_tax_2(receipt_pred):
    # working example
    receipt_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 10.2, "confidence": 0.5},
        {"rate": 10, "value": 40.0, "confidence": 0.1},
    ]
    financial_doc = FinancialV1(receipt_pred)
    assert financial_doc.total_tax.value == 50.2
    assert financial_doc.total_tax.confidence == 0.05


def test__receipt_taxes_match_total_incl_1(receipt_pred):
    # matching example
    receipt_pred["prediction"]["total_incl"] = {"value": 507.25, "confidence": 0.6}
    receipt_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 10.99, "confidence": 0.5},
        {"rate": 10, "value": 40.12, "confidence": 0.1},
    ]
    financial_doc = FinancialV1(receipt_pred)
    assert financial_doc.checklist["taxes_match_total_incl"] is True
    assert financial_doc.total_incl.confidence == 1.0
    for tax in financial_doc.taxes:
        assert tax.confidence == 1.0


def test__receipt_taxes_match_total_incl_2(receipt_pred):
    # not matching example with close error
    receipt_pred["prediction"]["total_incl"] = {"value": 507.25, "confidence": 0.6}
    receipt_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 10.9, "confidence": 0.5},
        {"rate": 10, "value": 40.12, "confidence": 0.1},
    ]
    financial_doc = FinancialV1(receipt_pred)
    assert financial_doc.checklist["taxes_match_total_incl"] is False


def test__receipt_taxes_match_total_incl_3(receipt_pred):
    # sanity check with null tax
    receipt_pred["prediction"]["total_incl"] = {"value": 507.25, "confidence": 0.6}
    receipt_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 0.0, "confidence": 0.5}
    ]
    financial_doc = FinancialV1(receipt_pred)
    assert financial_doc.checklist["taxes_match_total_incl"] is False


# Business tests from invoice
def test__invoice_reconstruct_total_excl_from_total_and_taxes_1(invoice_pred):
    # no incl implies no reconstruct for total excl
    invoice_pred["prediction"]["total_incl"] = {"amount": "N/A", "confidence": 0.0}
    invoice_pred["prediction"]["taxes"] = [
        {"rate": 20, "amount": 9.5, "confidence": 0.9}
    ]
    financial_doc = FinancialV1(invoice_pred)
    assert financial_doc.total_excl.value is None


def test__invoice_reconstruct_total_excl_from_total_and_taxes_2(invoice_pred):
    # no taxes implies no reconstruct for total excl
    invoice_pred["prediction"]["total_incl"] = {"amount": 12.54, "confidence": 0.0}
    invoice_pred["prediction"]["taxes"] = []
    financial_doc = FinancialV1(invoice_pred)
    assert financial_doc.total_excl.value is None


def test__invoice_reconstruct_total_excl_from_total_and_taxes_3(invoice_pred):
    # working example
    invoice_pred["prediction"]["total_incl"] = {"value": 12.54, "confidence": 0.5}
    invoice_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 0.5, "confidence": 0.1},
        {"rate": 10, "value": 4.25, "confidence": 0.6},
    ]
    financial_doc = FinancialV1(invoice_pred)
    assert financial_doc.total_excl.confidence == 0.03
    assert financial_doc.total_excl.value == 7.79


def test__invoice_reconstruct_total_tax_1(invoice_pred):
    # no taxes implies no reconstruct for total tax
    invoice_pred["prediction"]["taxes"] = []
    financial_doc = FinancialV1(invoice_pred)
    assert financial_doc.total_tax.value is None


def test__invoice_reconstruct_total_tax_2(invoice_pred):
    # working example
    invoice_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 10.2, "confidence": 0.5},
        {"rate": 10, "value": 40.0, "confidence": 0.1},
    ]
    financial_doc = FinancialV1(invoice_pred)
    assert financial_doc.total_tax.value == 50.2
    assert financial_doc.total_tax.confidence == 0.05


def test__invoice_taxes_match_total_incl_1(invoice_pred):
    # matching example
    invoice_pred["prediction"]["total_incl"] = {"value": 507.25, "confidence": 0.6}
    invoice_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 10.99, "confidence": 0.5},
        {"rate": 10, "value": 40.12, "confidence": 0.1},
    ]
    financial_doc = FinancialV1(invoice_pred)
    assert financial_doc.checklist["taxes_match_total_incl"] is True
    assert financial_doc.total_incl.confidence == 1.0
    for tax in financial_doc.taxes:
        assert tax.confidence == 1.0


def test__invoice_taxes_match_total_incl_2(invoice_pred):
    # not matching example with close error
    invoice_pred["prediction"]["total_incl"] = {"value": 507.25, "confidence": 0.6}
    invoice_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 10.9, "confidence": 0.5},
        {"rate": 10, "value": 40.12, "confidence": 0.1},
    ]
    financial_doc = FinancialV1(invoice_pred)
    assert financial_doc.checklist["taxes_match_total_incl"] is False


def test__invoice_taxes_match_total_incl_3(invoice_pred):
    # sanity check with null tax
    invoice_pred["prediction"]["total_incl"] = {"value": 507.25, "confidence": 0.6}
    invoice_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 0.0, "confidence": 0.5}
    ]
    financial_doc = FinancialV1(invoice_pred)
    assert financial_doc.checklist["taxes_match_total_incl"] is False


def test__shouldnt_raise_when_tax_rate_none(invoice_pred):
    # sanity check with null tax
    invoice_pred["prediction"]["total_incl"] = {"value": 507.25, "confidence": 0.6}
    invoice_pred["prediction"]["taxes"] = [
        {"rate": "N/A", "value": 0.0, "confidence": 0.5}
    ]
    financial_doc = FinancialV1(invoice_pred)
    assert financial_doc.checklist["taxes_match_total_incl"] is False


def test_invoice_or_receipt_get_same_field_types(receipt_pred, invoice_pred):
    financial_doc_from_receipt = FinancialV1(receipt_pred)
    financial_doc_from_invoice = FinancialV1(invoice_pred)
    assert set(dir(financial_doc_from_invoice)) == set(dir(financial_doc_from_receipt))
    for key in dir(financial_doc_from_receipt):
        if key.startswith("_"):
            continue
        receipt_attr = getattr(financial_doc_from_receipt, key)
        invoice_attr = getattr(financial_doc_from_invoice, key)
        print(key)
        assert isinstance(
            receipt_attr, type(invoice_attr)
        ), f"Types do not match for: {key}"
