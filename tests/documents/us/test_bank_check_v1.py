import json

import pytest

from mindee.documents.us.bank_check.bank_check_v1 import BankCheckV1
from tests import US_BANK_CHECK_DATA_DIR

FILE_PATH_US_BANK_CHECK_V1_COMPLETE = (
    f"{US_BANK_CHECK_DATA_DIR}/response_v1/complete.json"
)
FILE_PATH_US_BANK_CHECK_V1_EMPTY = f"{US_BANK_CHECK_DATA_DIR}/response_v1/empty.json"


@pytest.fixture
def bank_check_v1_doc_object() -> BankCheckV1:
    json_data = json.load(open(FILE_PATH_US_BANK_CHECK_V1_COMPLETE))
    return BankCheckV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def bank_check_v1_doc_object_empty() -> BankCheckV1:
    json_data = json.load(open(FILE_PATH_US_BANK_CHECK_V1_EMPTY))
    return BankCheckV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def bank_check_pred():
    json_data = json.load(open(FILE_PATH_US_BANK_CHECK_V1_EMPTY))
    return json_data["document"]["inference"]["pages"][0]


# Technical tests
def test_constructor(bank_check_v1_doc_object):
    assert bank_check_v1_doc_object.date.value == "2022-04-26"
    assert bank_check_v1_doc_object.amount.value == 6496.58
    assert bank_check_v1_doc_object.routing_number.value == "012345678"
    assert bank_check_v1_doc_object.account_number.value == "12345678910"
    assert bank_check_v1_doc_object.check_number.value == "8620001342"
    doc_str = (
        open(f"{US_BANK_CHECK_DATA_DIR}/response_v1/doc_to_string.txt").read().strip()
    )
    assert str(bank_check_v1_doc_object) == doc_str


def test_all_na(bank_check_v1_doc_object_empty):
    assert bank_check_v1_doc_object_empty.amount.value is None
    assert bank_check_v1_doc_object_empty.date.value is None
    assert bank_check_v1_doc_object_empty.check_number.value is None
    assert bank_check_v1_doc_object_empty.routing_number.value is None
    assert bank_check_v1_doc_object_empty.account_number.value is None
    assert len(bank_check_v1_doc_object_empty.signatures_positions) == 0
    assert len(bank_check_v1_doc_object_empty.check_position.polygon) == 0
    assert len(bank_check_v1_doc_object_empty.check_position.value) == 0
    assert bank_check_v1_doc_object_empty.check_position.bounding_box is None
    assert bank_check_v1_doc_object_empty.check_position.rectangle is None
    assert bank_check_v1_doc_object_empty.check_position.quadrangle is None
    assert len(bank_check_v1_doc_object_empty.payees) == 0
