import json
import pytest
from mindee import Passport


@pytest.fixture
def passport_object():
    json_repsonse = json.load(open("./tests/data/passport/v1/passport.json"))
    return Passport(json_repsonse["predictions"][0])


@pytest.fixture
def passport_object_from_scratch():
    return Passport(
        country="FR",
        id_number="sqd12354",
        birth_date="1989-10-19",
        expiry_date="2027-12-01",
        issuance_date="2017-11-31",
        birth_place="Paris",
        gender="M",
        surname="Doe",
        mrz1="P<GBRPUDARSAN<<HENERT<<<<<<<<<<<<<<<<<<<<<<<",
        mrz2="7077979792GBR9505209M1704224<<<<<<<<<<<<<<00",
        given_names=["John", "Jane"],
        mrz="P<GBRPUDARSAN<<HENERT<<<<<<<<<<<<<<<<<<<<<<<7077979792GBR9505209M1704224<<<<<<<<<<<<<<00",
        full_name="John Doe"
    )


@pytest.fixture
def passport_object_all_na():
    json_repsonse = json.load(open("./tests/data/passport/v1/passport_all_na.json"))
    return Passport(json_repsonse["predictions"][0])


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


def test_compare_1(passport_object):
    # Compare same object must return all True
    benchmark = Passport.compare(passport_object, passport_object)
    for value in benchmark.values():
        assert value is True


def test_compare_3(passport_object, passport_object_all_na):
    # Compare full object and empty object
    benchmark = Passport.compare(passport_object, passport_object_all_na)
    for value in benchmark.values():
        assert value is False


def test_compare_5(passport_object_from_scratch):
    # Compare passport from class
    benchmark = Passport.compare(passport_object_from_scratch, passport_object_from_scratch)
    for key in benchmark.keys():
        if "__acc__" in key:
            assert benchmark[key] is True


def test_compare_6(passport_object_from_scratch):
    # Compare passport from class with empty given_names
    passport_object_from_scratch.given_names = []
    benchmark = Passport.compare(passport_object_from_scratch, passport_object_from_scratch)
    for key in benchmark.keys():
        if "__acc__" in key:
            assert benchmark[key] is True
        elif "__pre__" in key:
            assert benchmark[key] in [True, None]


def test_empty_object_works():
    passport = Passport()
    assert passport.full_name.value is None

