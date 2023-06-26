import json

import pytest

from mindee.documents import PassportV1

PASSPORT_DATA_DIR = "./tests/data/passport"
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
    file_path = f"{ PASSPORT_DATA_DIR }/response_v1/doc_to_string.txt"
    reference_str = open(file_path, "r", encoding="utf-8").read().strip()
    assert str(passport_v1_doc) == reference_str


def test_page0_constructor(passport_v1_page0):
    file_path = f"{ PASSPORT_DATA_DIR }/response_v1/page0_to_string.txt"
    reference_str = open(file_path, "r", encoding="utf-8").read().strip()
    assert str(passport_v1_page0) == reference_str


def test_checklist_all_na(passport_v1_doc_empty):
    for check in passport_v1_doc_empty.checklist.values():
        assert check is False


def test_checksum():
    mrz = "7077979792GBR9505209M1704224<<<<<<<<<<<<<<00"
    assert PassportV1.check_sum(mrz[0:10] + mrz[13:20] + mrz[21:43]) == mrz[43]


def test_wrong_checksum():
    mrz = "7077974792GBR9505209M1704224<<<<<<<<<<<<<<00"
    assert PassportV1.check_sum(mrz[0:10] + mrz[13:20] + mrz[21:43]) != mrz[43]
    mrz = "7077974792GBR9505209M1404224<<<<<<<<<<<<<<00"
    assert PassportV1.check_sum(mrz[0:10] + mrz[13:20] + mrz[21:43]) != mrz[43]
    mrz = "7077974792GBR9505209M1404224<<<<<<<<<<<<<<08"
    assert PassportV1.check_sum(mrz[0:10] + mrz[13:20] + mrz[21:43]) != mrz[43]


def test_checksum_with_personal_number_alpha():
    mrz = "XDB0661884ESP9502138F1808122RE20050024133894"
    assert PassportV1.check_sum(mrz[28:42]) == mrz[42]
