import json

import pytest

from mindee.documents.passport import Passport


@pytest.fixture
def passport_object():
    json_repsonse = json.load(open("./tests/data/passport/v1/passport.json"))
    return Passport(json_repsonse["document"]["inference"]["pages"][0]["prediction"])


@pytest.fixture
def passport_object_all_na():
    json_repsonse = json.load(open("./tests/data/passport/v1/passport_all_na.json"))
    return Passport(json_repsonse["document"]["inference"]["pages"][0]["prediction"])


def test_constructor(passport_object):
    assert passport_object.mrz1.value == "P<GBRPUDARSAN<<HENERT<<<<<<<<<<<<<<<<<<<<<<<"
    assert passport_object.mrz2.value == "7077979792GBR9505209M1704224<<<<<<<<<<<<<<00"
    assert passport_object.id_number.value == "707797979"
    assert type(passport_object.__str__()) == str
    assert passport_object.is_expired()
    assert passport_object.all_checks()


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
    assert Passport.check_sum(mrz[0:10] + mrz[13:20] + mrz[21:43]) == mrz[43]


def test_wrong_checksum():
    mrz = "7077974792GBR9505209M1704224<<<<<<<<<<<<<<00"
    assert Passport.check_sum(mrz[0:10] + mrz[13:20] + mrz[21:43]) != mrz[43]
    mrz = "7077974792GBR9505209M1404224<<<<<<<<<<<<<<00"
    assert Passport.check_sum(mrz[0:10] + mrz[13:20] + mrz[21:43]) != mrz[43]
    mrz = "7077974792GBR9505209M1404224<<<<<<<<<<<<<<08"
    assert Passport.check_sum(mrz[0:10] + mrz[13:20] + mrz[21:43]) != mrz[43]


def test_checksum_with_personal_number_alpha():
    mrz = "XDB0661884ESP9502138F1808122RE20050024133894"
    assert Passport.check_sum(mrz[28:42]) == mrz[42]
