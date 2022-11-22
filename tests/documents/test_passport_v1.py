import json

import pytest

from mindee.documents.passport.passport_v1 import PassportV1
from tests import PASSPORT_DATA_DIR

FILE_PATH_PASSPORT_V1_COMPLETE = f"{PASSPORT_DATA_DIR}/response_v1/complete.json"


@pytest.fixture
def passport_v1_doc_object():
    json_data = json.load(open(FILE_PATH_PASSPORT_V1_COMPLETE))
    return PassportV1(api_prediction=json_data["document"]["inference"], page_n=None)


@pytest.fixture
def passport_v1_doc_object_empty():
    json_data = json.load(open(f"{PASSPORT_DATA_DIR}/response_v1/empty.json"))
    return PassportV1(api_prediction=json_data["document"]["inference"], page_n=None)


@pytest.fixture
def passport_v1_page_object():
    json_data = json.load(open(FILE_PATH_PASSPORT_V1_COMPLETE))
    return PassportV1(
        api_prediction=json_data["document"]["inference"]["pages"][0], page_n=0
    )


def test_constructor(passport_v1_doc_object):
    assert not passport_v1_doc_object.is_expired()
    assert passport_v1_doc_object.all_checks()
    doc_str = (
        open(f"{PASSPORT_DATA_DIR}/response_v1/page0_to_string.txt").read().strip()
    )
    assert passport_v1_doc_object.birth_date.page_n == 0
    assert str(passport_v1_doc_object) == doc_str


def test_page_constructor(passport_v1_page_object):
    doc_str = (
        open(f"{PASSPORT_DATA_DIR}/response_v1/page0_to_string.txt").read().strip()
    )
    assert passport_v1_page_object.orientation.value == 0
    assert passport_v1_page_object.birth_date.page_n == 0
    assert str(passport_v1_page_object) == doc_str
    assert len(passport_v1_page_object.cropper) == 0


def test_all_na(passport_v1_doc_object_empty):
    assert passport_v1_doc_object_empty.mrz.value is None
    assert passport_v1_doc_object_empty.country.value is None
    assert passport_v1_doc_object_empty.id_number.value is None
    assert passport_v1_doc_object_empty.birth_date.value is None
    assert passport_v1_doc_object_empty.expiry_date.value is None
    assert passport_v1_doc_object_empty.issuance_date.value is None
    assert passport_v1_doc_object_empty.birth_place.value is None
    assert passport_v1_doc_object_empty.gender.value is None
    assert passport_v1_doc_object_empty.surname.value is None
    assert passport_v1_doc_object_empty.mrz1.value is None
    assert passport_v1_doc_object_empty.mrz2.value is None
    assert len(passport_v1_doc_object_empty.given_names) == 0


def test_checklist(passport_v1_doc_object):
    for check in passport_v1_doc_object.checklist.values():
        assert check is True


def test_checklist_all_na(passport_v1_doc_object_empty):
    for check in passport_v1_doc_object_empty.checklist.values():
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
