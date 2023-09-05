import json

import pytest

from mindee.documents.fr import BankAccountDetailsV2

FR_BANK_ACCOUNT_DETAILS_DATA_DIR = "./tests/data/products/bank_account_details"
FILE_PATH_FR_BANK_ACCOUNT_DETAILS_V2_COMPLETE = (
    f"{ FR_BANK_ACCOUNT_DETAILS_DATA_DIR }/response_v2/complete.json"
)
FILE_PATH_FR_BANK_ACCOUNT_DETAILS_V2_EMPTY = (
    f"{ FR_BANK_ACCOUNT_DETAILS_DATA_DIR }/response_v2/empty.json"
)


@pytest.fixture
def bank_account_details_v2_doc() -> BankAccountDetailsV2:
    json_data = json.load(open(FILE_PATH_FR_BANK_ACCOUNT_DETAILS_V2_COMPLETE))
    return BankAccountDetailsV2(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def bank_account_details_v2_doc_empty() -> BankAccountDetailsV2:
    json_data = json.load(open(FILE_PATH_FR_BANK_ACCOUNT_DETAILS_V2_EMPTY))
    return BankAccountDetailsV2(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def bank_account_details_v2_page0():
    json_data = json.load(open(FILE_PATH_FR_BANK_ACCOUNT_DETAILS_V2_COMPLETE))
    return BankAccountDetailsV2(
        json_data["document"]["inference"]["pages"][0], page_n=0
    )


def test_empty_doc_constructor(bank_account_details_v2_doc_empty):
    assert bank_account_details_v2_doc_empty.account_holders_names.value is None
    assert bank_account_details_v2_doc_empty.bban.bban_bank_code is None
    assert bank_account_details_v2_doc_empty.bban.bban_branch_code is None
    assert bank_account_details_v2_doc_empty.bban.bban_key is None
    assert bank_account_details_v2_doc_empty.bban.bban_number is None
    assert bank_account_details_v2_doc_empty.iban.value is None
    assert bank_account_details_v2_doc_empty.swift_code.value is None


def test_doc_constructor(bank_account_details_v2_doc):
    file_path = f"{ FR_BANK_ACCOUNT_DETAILS_DATA_DIR }/response_v2/doc_to_string.rst"
    reference_str = open(file_path, "r", encoding="utf-8").read()
    assert str(bank_account_details_v2_doc) == reference_str


def test_page0_constructor(bank_account_details_v2_page0):
    file_path = f"{ FR_BANK_ACCOUNT_DETAILS_DATA_DIR }/response_v2/page0_to_string.rst"
    reference_str = open(file_path, "r", encoding="utf-8").read()
    assert str(bank_account_details_v2_page0) == reference_str
