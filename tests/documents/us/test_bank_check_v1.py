import json

import pytest

from mindee.documents.us import BankCheckV1

US_BANK_CHECK_DATA_DIR = "./tests/data/us/bank_check"
FILE_PATH_US_BANK_CHECK_V1_COMPLETE = (
    f"{ US_BANK_CHECK_DATA_DIR }/response_v1/complete.json"
)
FILE_PATH_US_BANK_CHECK_V1_EMPTY = f"{ US_BANK_CHECK_DATA_DIR }/response_v1/empty.json"


@pytest.fixture
def bank_check_v1_doc() -> BankCheckV1:
    json_data = json.load(open(FILE_PATH_US_BANK_CHECK_V1_COMPLETE))
    return BankCheckV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def bank_check_v1_doc_empty() -> BankCheckV1:
    json_data = json.load(open(FILE_PATH_US_BANK_CHECK_V1_EMPTY))
    return BankCheckV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def bank_check_v1_page0():
    json_data = json.load(open(FILE_PATH_US_BANK_CHECK_V1_COMPLETE))
    return BankCheckV1(json_data["document"]["inference"]["pages"][0], page_n=0)


def test_empty_doc_constructor(bank_check_v1_doc_empty):
    assert bank_check_v1_doc_empty.check_position.value == []
    assert len(bank_check_v1_doc_empty.signatures_positions) == 0
    assert bank_check_v1_doc_empty.date.value is None
    assert bank_check_v1_doc_empty.amount.value is None
    assert len(bank_check_v1_doc_empty.payees) == 0
    assert bank_check_v1_doc_empty.routing_number.value is None
    assert bank_check_v1_doc_empty.account_number.value is None
    assert bank_check_v1_doc_empty.check_number.value is None


# Technical tests
def test_constructor(bank_check_v1_doc):
    assert bank_check_v1_doc.date.value == "2022-04-26"
    assert bank_check_v1_doc.amount.value == 6496.58
    assert bank_check_v1_doc.routing_number.value == "012345678"
    assert bank_check_v1_doc.account_number.value == "12345678910"
    assert bank_check_v1_doc.check_number.value == "8620001342"
    doc_str = (
        open(f"{US_BANK_CHECK_DATA_DIR}/response_v1/doc_to_string.txt").read().strip()
    )
    assert str(bank_check_v1_doc) == doc_str
