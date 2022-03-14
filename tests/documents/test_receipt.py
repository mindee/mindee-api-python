import json

import pytest

from mindee.documents.receipt import Receipt

RECEIPT_FILE_PATH = "./tests/data/expense_receipts/v3/receipt.json"
RECEIPT_NA_FILE_PATH = "./tests/data/expense_receipts/v3/receipt_all_na.json"


@pytest.fixture
def receipt_object():
    json_response = json.load(open(RECEIPT_FILE_PATH))
    return Receipt(json_response["document"]["inference"]["prediction"], page_n=None)


@pytest.fixture
def receipt_object_all_na():
    json_response = json.load(open(RECEIPT_NA_FILE_PATH))
    return Receipt(json_response["document"]["inference"]["prediction"], page_n=None)


@pytest.fixture
def receipt_pred():
    json_response = json.load(open(RECEIPT_NA_FILE_PATH))
    return json_response["document"]["inference"]["pages"][0]["prediction"]


# Technical tests
def test_constructor(receipt_object):
    assert receipt_object.date.value == "2016-02-26"
    assert receipt_object.total_tax.value == 1.7
    assert receipt_object.checklist["taxes_match_total_incl"] is True
    assert (
        str(receipt_object)
        == """-----Receipt data-----
Filename: None
Total amount including taxes: 10.2
Total amount excluding taxes: 8.5
Date: 2016-02-26
Category: food
Time: 15:20
Merchant name: CLACHAN
Taxes: 1.7 20.0%
Total taxes: 1.7
Locale: en-GB; en; GB; GBP;
----------------------"""
    )


def test_all_na(receipt_object_all_na):
    assert receipt_object_all_na.locale.value is None
    assert receipt_object_all_na.total_incl.value is None
    assert receipt_object_all_na.date.value is None
    assert receipt_object_all_na.merchant_name.value is None
    assert receipt_object_all_na.time.value is None
    assert receipt_object_all_na.orientation is None
    assert receipt_object_all_na.total_tax.value is None
    assert len(receipt_object_all_na.taxes) == 0


def test_checklist_on_empty(receipt_object_all_na):
    for check in receipt_object_all_na.checklist.values():
        assert check is False


# Business tests
def test__reconstruct_total_excl_from_total_and_taxes_1(receipt_pred):
    # no incl implies no reconstruct for total excl
    receipt_pred["total_incl"] = {"value": "N/A", "confidence": 0.0}
    receipt_pred["taxes"] = [{"rate": 20, "value": 9.5, "confidence": 0.9}]
    receipt = Receipt(receipt_pred)
    assert receipt.total_excl.value is None


def test__reconstruct_total_excl_from_total_and_taxes_2(receipt_pred):
    # no taxes implies no reconstruct for total excl
    receipt_pred["total_incl"] = {"value": 12.54, "confidence": 0.0}
    receipt_pred["taxes"] = []
    receipt = Receipt(receipt_pred)
    assert receipt.total_excl.value is None


def test__reconstruct_total_excl_from_total_and_taxes_3(receipt_pred):
    # working example
    receipt_pred["total_incl"] = {"value": 12.54, "confidence": 0.5}
    receipt_pred["taxes"] = [
        {"rate": 20, "value": 0.5, "confidence": 0.1},
        {"rate": 10, "value": 4.25, "confidence": 0.6},
    ]
    receipt = Receipt(receipt_pred)
    assert receipt.total_excl.confidence == 0.03
    assert receipt.total_excl.value == 7.79


def test__reconstruct_total_tax_1(receipt_pred):
    # no taxes implies no reconstruct for total tax
    receipt_pred["taxes"] = []
    receipt = Receipt(receipt_pred)
    assert receipt.total_tax.value is None


def test__reconstruct_total_tax_2(receipt_pred):
    # working example
    receipt_pred["taxes"] = [
        {"rate": 20, "value": 10.2, "confidence": 0.5},
        {"rate": 10, "value": 40.0, "confidence": 0.1},
    ]
    receipt = Receipt(receipt_pred)
    assert receipt.total_tax.value == 50.2
    assert receipt.total_tax.confidence == 0.05


def test__taxes_match_total_incl_1(receipt_pred):
    # matching example
    receipt_pred["total_incl"] = {"value": 507.25, "confidence": 0.6}
    receipt_pred["taxes"] = [
        {"rate": 20, "value": 10.99, "confidence": 0.5},
        {"rate": 10, "value": 40.12, "confidence": 0.1},
    ]
    receipt = Receipt(receipt_pred)
    assert receipt.checklist["taxes_match_total_incl"] is True
    assert receipt.total_incl.confidence == 1.0
    for tax in receipt.taxes:
        assert tax.confidence == 1.0


def test__taxes_match_total_incl_2(receipt_pred):
    # not matching example with close error
    receipt_pred["total_incl"] = {"value": 507.25, "confidence": 0.6}
    receipt_pred["taxes"] = [
        {"rate": 20, "value": 10.9, "confidence": 0.5},
        {"rate": 10, "value": 40.12, "confidence": 0.1},
    ]
    receipt = Receipt(receipt_pred)
    assert receipt.checklist["taxes_match_total_incl"] is False


def test__taxes_match_total_incl_3(receipt_pred):
    # sanity check with null tax
    receipt_pred["total_incl"] = {"value": 507.25, "confidence": 0.6}
    receipt_pred["taxes"] = [{"rate": 20, "value": 0.0, "confidence": 0.5}]
    receipt = Receipt(receipt_pred)
    assert receipt.checklist["taxes_match_total_incl"] is False


def test__taxes_match_total_incl_4(receipt_pred):
    # sanity check with None tax rate
    receipt_pred["total_incl"] = {"value": 507.25, "confidence": 0.6}
    receipt_pred["taxes"] = [{"rate": "N/A", "value": 0.0, "confidence": 0.5}]
    receipt = Receipt(receipt_pred)
    assert receipt.checklist["taxes_match_total_incl"] is False
    assert type(str(receipt.taxes[0])) is str


def test_null_tax_rates_dont_raise(receipt_pred):
    receipt_pred["total_excl"] = {"value": 12, "confidence": 0.6}
    receipt_pred["total_incl"] = {"value": 15, "confidence": 0.6}
    receipt_pred["taxes"] = [
        {"rate": 1, "value": 0.0, "confidence": 0.5},
        {"rate": 2, "value": 20.0, "confidence": 0.5},
    ]
    receipt = Receipt(receipt_pred)
    assert receipt.checklist["taxes_match_total_incl"] is False
