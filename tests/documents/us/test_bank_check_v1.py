import json

import pytest

from mindee.documents.us import BankCheckV1

US_BANK_CHECK_DATA_DIR = "./tests/data/products/bank_check"
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
    assert bank_check_v1_doc_empty.check_position.value is None
    assert len(bank_check_v1_doc_empty.signatures_positions) == 0
    assert bank_check_v1_doc_empty.date.value is None
    assert bank_check_v1_doc_empty.amount.value is None
    assert len(bank_check_v1_doc_empty.payees) == 0
    assert bank_check_v1_doc_empty.routing_number.value is None
    assert bank_check_v1_doc_empty.account_number.value is None
    assert bank_check_v1_doc_empty.check_number.value is None


def test_doc_constructor(bank_check_v1_doc):
    file_path = f"{ US_BANK_CHECK_DATA_DIR }/response_v1/doc_to_string.rst"
    reference_str = open(file_path, "r", encoding="utf-8").read()
    assert str(bank_check_v1_doc) == reference_str


def test_page0_constructor(bank_check_v1_page0):
    file_path = f"{ US_BANK_CHECK_DATA_DIR }/response_v1/page0_to_string.rst"
    reference_str = open(file_path, "r", encoding="utf-8").read()
    assert str(bank_check_v1_page0) == reference_str
