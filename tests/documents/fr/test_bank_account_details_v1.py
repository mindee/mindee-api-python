import json

import pytest

from mindee.documents.fr import BankAccountDetailsV1

FR_BANK_ACCOUNT_DETAILS_DATA_DIR = "./tests/data/products/bank_account_details"
FILE_PATH_FR_BANK_ACCOUNT_DETAILS_V1_COMPLETE = (
    f"{ FR_BANK_ACCOUNT_DETAILS_DATA_DIR }/response_v1/complete.json"
)
FILE_PATH_FR_BANK_ACCOUNT_DETAILS_V1_EMPTY = (
    f"{ FR_BANK_ACCOUNT_DETAILS_DATA_DIR }/response_v1/empty.json"
)


@pytest.fixture
def bank_account_details_v1_doc() -> BankAccountDetailsV1:
    json_data = json.load(open(FILE_PATH_FR_BANK_ACCOUNT_DETAILS_V1_COMPLETE))
    return BankAccountDetailsV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def bank_account_details_v1_doc_empty() -> BankAccountDetailsV1:
    json_data = json.load(open(FILE_PATH_FR_BANK_ACCOUNT_DETAILS_V1_EMPTY))
    return BankAccountDetailsV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def bank_account_details_v1_page0():
    json_data = json.load(open(FILE_PATH_FR_BANK_ACCOUNT_DETAILS_V1_COMPLETE))
    return BankAccountDetailsV1(
        json_data["document"]["inference"]["pages"][0], page_n=0
    )


def test_empty_doc_constructor(bank_account_details_v1_doc_empty):
    assert bank_account_details_v1_doc_empty.iban.value is None
    assert bank_account_details_v1_doc_empty.account_holder_name.value is None
    assert bank_account_details_v1_doc_empty.swift.value is None


def test_doc_constructor(bank_account_details_v1_doc):
    file_path = f"{ FR_BANK_ACCOUNT_DETAILS_DATA_DIR }/response_v1/doc_to_string.rst"
    reference_str = open(file_path, "r", encoding="utf-8").read()
    assert str(bank_account_details_v1_doc) == reference_str


def test_page0_constructor(bank_account_details_v1_page0):
    file_path = f"{ FR_BANK_ACCOUNT_DETAILS_DATA_DIR }/response_v1/page0_to_string.rst"
    reference_str = open(file_path, "r", encoding="utf-8").read()
    assert str(bank_account_details_v1_page0) == reference_str
