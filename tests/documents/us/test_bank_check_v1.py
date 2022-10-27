import json

import pytest

from mindee.documents.us.bank_check.bank_check_v1 import BankCheckV1
from tests import BANK_CHECK_DATA_DIR

BANK_CHECK_FILE_PATH = f"{BANK_CHECK_DATA_DIR}/response_v1/complete.json"
BANK_CHECK_NA_FILE_PATH = f"{BANK_CHECK_DATA_DIR}/response_v1/empty.json"


@pytest.fixture
def doc_object():
    json_data = json.load(open(BANK_CHECK_FILE_PATH))
    return BankCheckV1(json_data["document"]["inference"]["prediction"], page_n=None)


@pytest.fixture
def bank_check_object_all_na():
    json_data = json.load(open(BANK_CHECK_NA_FILE_PATH))
    return BankCheckV1(json_data["document"]["inference"]["prediction"], page_n=None)


@pytest.fixture
def bank_check_pred():
    json_data = json.load(open(BANK_CHECK_NA_FILE_PATH))
    return json_data["document"]["inference"]["pages"][0]["prediction"]


# Technical tests
def test_constructor(doc_object):
    assert doc_object.date.value == "2022-04-26"
    assert doc_object.amount.value == 6496.58
    assert doc_object.routing_number.value == "012345678"
    assert doc_object.account_number.value == "12345678910"
    assert doc_object.check_number.value == "8620001342"
    doc_str = (
        open(f"{BANK_CHECK_DATA_DIR}/response_v1/doc_to_string.txt").read().strip()
    )
    assert str(doc_object) == doc_str


def test_all_na(bank_check_object_all_na):
    assert bank_check_object_all_na.amount.value is None
    assert bank_check_object_all_na.date.value is None
    assert bank_check_object_all_na.check_number.value is None
    assert bank_check_object_all_na.routing_number.value is None
    assert bank_check_object_all_na.account_number.value is None
    assert len(bank_check_object_all_na.signatures_positions) == 0
    assert len(bank_check_object_all_na.check_position.polygon) == 0
    assert len(bank_check_object_all_na.check_position.value) == 0
    assert bank_check_object_all_na.check_position.bounding_box is None
    assert bank_check_object_all_na.check_position.rectangle is None
    assert bank_check_object_all_na.check_position.quadrangle is None
    assert len(bank_check_object_all_na.payees) == 0
