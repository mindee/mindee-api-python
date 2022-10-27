import json

import pytest

from mindee.documents.passport.passport_v1 import PassportV1
from tests import PASSPORT_DATA_DIR

PASSPORT_FILE_PATH = f"{PASSPORT_DATA_DIR}/response_v1/complete.json"


@pytest.fixture
def passport_object():
    json_data = json.load(open(PASSPORT_FILE_PATH))
    return PassportV1(json_data["document"]["inference"]["pages"][0]["prediction"])


@pytest.fixture
def passport_object_all_na():
    json_data = json.load(open(f"{PASSPORT_DATA_DIR}/response_v1/empty.json"))
    return PassportV1(json_data["document"]["inference"]["pages"][0]["prediction"])


def test_constructor(passport_object):
    assert not passport_object.is_expired()
    assert passport_object.all_checks()
    doc_str = (
        open(f"{PASSPORT_DATA_DIR}/response_v1/page0_to_string.txt").read().strip()
    )
    assert str(passport_object) == doc_str


def test_all_na(passport_object_all_na):
    assert passport_object_all_na.mrz.value is None
    assert passport_object_all_na.country.value is None
    assert passport_object_all_na.id_number.value is None
    assert passport_object_all_na.birth_date.value is None
    assert passport_object_all_na.expiry_date.value is None
    assert passport_object_all_na.issuance_date.value is None
    assert passport_object_all_na.birth_place.value is None
    assert passport_object_all_na.gender.value is None
    assert passport_object_all_na.surname.value is None
    assert passport_object_all_na.mrz1.value is None
    assert passport_object_all_na.mrz2.value is None
    assert len(passport_object_all_na.given_names) == 0


def test_checklist(passport_object):
    for check in passport_object.checklist.values():
        assert check is True


def test_checklist_all_na(passport_object_all_na):
    for check in passport_object_all_na.checklist.values():
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
