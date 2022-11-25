import json

import pytest

from mindee.documents.receipt.receipt_v3 import ReceiptV3
from tests import RECEIPT_DATA_DIR

FILE_PATH_RECEIPT_V3_COMPLETE = f"{RECEIPT_DATA_DIR}/response_v3/complete.json"
FILE_PATH_RECEIPT_V3_EMPTY = f"{RECEIPT_DATA_DIR}/response_v3/empty.json"


@pytest.fixture
def receipt_v3_doc_object():
    json_data = json.load(open(FILE_PATH_RECEIPT_V3_COMPLETE))
    return ReceiptV3(api_prediction=json_data["document"]["inference"], page_n=None)


@pytest.fixture
def receipt_v3_doc_object_empty():
    json_data = json.load(open(FILE_PATH_RECEIPT_V3_EMPTY))
    return ReceiptV3(api_prediction=json_data["document"]["inference"], page_n=None)


@pytest.fixture
def receipt_pred():
    json_data = json.load(open(FILE_PATH_RECEIPT_V3_EMPTY))
    return json_data["document"]["inference"]["pages"][0]


def test_doc_constructor(receipt_v3_doc_object):
    assert receipt_v3_doc_object.date.value == "2016-02-26"
    assert receipt_v3_doc_object.total_tax.value == 1.7
    assert receipt_v3_doc_object.checklist["taxes_match_total_incl"] is True
    doc_str = open(f"{RECEIPT_DATA_DIR}/response_v3/doc_to_string.txt").read().strip()
    assert receipt_v3_doc_object.date.page_n == 0
    assert str(receipt_v3_doc_object) == doc_str


def test_all_na(receipt_v3_doc_object_empty):
    assert receipt_v3_doc_object_empty.locale.value is None
    assert receipt_v3_doc_object_empty.total_incl.value is None
    assert receipt_v3_doc_object_empty.date.value is None
    assert receipt_v3_doc_object_empty.merchant_name.value is None
    assert receipt_v3_doc_object_empty.time.value is None
    assert receipt_v3_doc_object_empty.orientation is None
    assert receipt_v3_doc_object_empty.total_tax.value is None
    assert len(receipt_v3_doc_object_empty.taxes) == 0


def test_checklist_on_empty(receipt_v3_doc_object_empty):
    for check in receipt_v3_doc_object_empty.checklist.values():
        assert check is False


# Business tests
def test__reconstruct_total_excl_from_total_and_taxes_1(receipt_pred):
    # no incl implies no reconstruct for total excl
    receipt_pred["prediction"]["total_incl"] = {"value": "N/A", "confidence": 0.0}
    receipt_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 9.5, "confidence": 0.9}
    ]
    receipt = ReceiptV3(receipt_pred)
    assert receipt.total_excl.value is None


def test__reconstruct_total_excl_from_total_and_taxes_2(receipt_pred):
    # no taxes implies no reconstruct for total excl
    receipt_pred["prediction"]["total_incl"] = {"value": 12.54, "confidence": 0.0}
    receipt_pred["prediction"]["taxes"] = []
    receipt = ReceiptV3(receipt_pred)
    assert receipt.total_excl.value is None


def test__reconstruct_total_excl_from_total_and_taxes_3(receipt_pred):
    # working example
    receipt_pred["prediction"]["total_incl"] = {"value": 12.54, "confidence": 0.5}
    receipt_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 0.5, "confidence": 0.1},
        {"rate": 10, "value": 4.25, "confidence": 0.6},
    ]
    receipt = ReceiptV3(receipt_pred)
    assert receipt.total_excl.confidence == 0.03
    assert receipt.total_excl.value == 7.79


def test__reconstruct_total_tax_1(receipt_pred):
    # no taxes implies no reconstruct for total tax
    receipt_pred["taxes"] = []
    receipt = ReceiptV3(receipt_pred)
    assert receipt.total_tax.value is None


def test__reconstruct_total_tax_2(receipt_pred):
    # working example
    receipt_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 10.2, "confidence": 0.5},
        {"rate": 10, "value": 40.0, "confidence": 0.1},
    ]
    receipt = ReceiptV3(receipt_pred)
    assert receipt.total_tax.value == 50.2
    assert receipt.total_tax.confidence == 0.05


def test__taxes_match_total_incl_1(receipt_pred):
    # matching example
    receipt_pred["prediction"]["total_incl"] = {"value": 507.25, "confidence": 0.6}
    receipt_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 10.99, "confidence": 0.5},
        {"rate": 10, "value": 40.12, "confidence": 0.1},
    ]
    receipt = ReceiptV3(receipt_pred)
    assert receipt.checklist["taxes_match_total_incl"] is True
    assert receipt.total_incl.confidence == 1.0
    for tax in receipt.taxes:
        assert tax.confidence == 1.0


def test__taxes_match_total_incl_2(receipt_pred):
    # not matching example with close error
    receipt_pred["prediction"]["total_incl"] = {"value": 507.25, "confidence": 0.6}
    receipt_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 10.9, "confidence": 0.5},
        {"rate": 10, "value": 40.12, "confidence": 0.1},
    ]
    receipt = ReceiptV3(receipt_pred)
    assert receipt.checklist["taxes_match_total_incl"] is False


def test__taxes_match_total_incl_3(receipt_pred):
    # sanity check with null tax
    receipt_pred["prediction"]["total_incl"] = {"value": 507.25, "confidence": 0.6}
    receipt_pred["prediction"]["taxes"] = [
        {"rate": 20, "value": 0.0, "confidence": 0.5}
    ]
    receipt = ReceiptV3(receipt_pred)
    assert receipt.checklist["taxes_match_total_incl"] is False


def test__taxes_match_total_incl_4(receipt_pred):
    # sanity check with None tax rate
    receipt_pred["prediction"]["total_incl"] = {"value": 507.25, "confidence": 0.6}
    receipt_pred["prediction"]["taxes"] = [
        {"rate": "N/A", "value": 0.0, "confidence": 0.5}
    ]
    receipt = ReceiptV3(receipt_pred)
    assert receipt.checklist["taxes_match_total_incl"] is False
    assert type(str(receipt.taxes[0])) is str


def test_null_tax_rates_dont_raise(receipt_pred):
    receipt_pred["prediction"]["total_excl"] = {"value": 12, "confidence": 0.6}
    receipt_pred["prediction"]["total_incl"] = {"value": 15, "confidence": 0.6}
    receipt_pred["prediction"]["taxes"] = [
        {"rate": 1, "value": 0.0, "confidence": 0.5},
        {"rate": 2, "value": 20.0, "confidence": 0.5},
    ]
    receipt = ReceiptV3(receipt_pred)
    assert receipt.checklist["taxes_match_total_incl"] is False
