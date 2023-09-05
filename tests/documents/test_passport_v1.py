import json

import pytest

from mindee.documents import PassportV1

PASSPORT_DATA_DIR = "./tests/data/products/passport"
FILE_PATH_PASSPORT_V1_COMPLETE = f"{ PASSPORT_DATA_DIR }/response_v1/complete.json"
FILE_PATH_PASSPORT_V1_EMPTY = f"{ PASSPORT_DATA_DIR }/response_v1/empty.json"


@pytest.fixture
def passport_v1_doc() -> PassportV1:
    json_data = json.load(open(FILE_PATH_PASSPORT_V1_COMPLETE))
    return PassportV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def passport_v1_doc_empty() -> PassportV1:
    json_data = json.load(open(FILE_PATH_PASSPORT_V1_EMPTY))
    return PassportV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def passport_v1_page0():
    json_data = json.load(open(FILE_PATH_PASSPORT_V1_COMPLETE))
    return PassportV1(json_data["document"]["inference"]["pages"][0], page_n=0)


def test_empty_doc_constructor(passport_v1_doc_empty):
    assert passport_v1_doc_empty.country.value is None
    assert passport_v1_doc_empty.id_number.value is None
    assert len(passport_v1_doc_empty.given_names) == 0
    assert passport_v1_doc_empty.surname.value is None
    assert passport_v1_doc_empty.birth_date.value is None
    assert passport_v1_doc_empty.birth_place.value is None
    assert passport_v1_doc_empty.gender.value is None
    assert passport_v1_doc_empty.issuance_date.value is None
    assert passport_v1_doc_empty.expiry_date.value is None
    assert passport_v1_doc_empty.mrz1.value is None
    assert passport_v1_doc_empty.mrz2.value is None


def test_doc_constructor(passport_v1_doc):
    file_path = f"{ PASSPORT_DATA_DIR }/response_v1/doc_to_string.rst"
    reference_str = open(file_path, "r", encoding="utf-8").read()
    assert str(passport_v1_doc) == reference_str


def test_page0_constructor(passport_v1_page0):
    file_path = f"{ PASSPORT_DATA_DIR }/response_v1/page0_to_string.rst"
    reference_str = open(file_path, "r", encoding="utf-8").read()
    assert str(passport_v1_page0) == reference_str
