import json

import pytest

from mindee import CarPlate


@pytest.fixture
def car_plate_object():
    json_repsonse = json.load(open("./tests/data/license_plates/v1/plate.json"))
    return CarPlate(json_repsonse["document"]["inference"]["pages"][0]["prediction"])


@pytest.fixture
def car_plate_object_from_scratch():
    return CarPlate(license_plates=["abcdef", "klimopo"])


@pytest.fixture
def car_plate_object_all_na():
    json_repsonse = json.load(open("./tests/data/license_plates/v1/plate_all_na.json"))
    return CarPlate(json_repsonse["document"]["inference"]["pages"][0]["prediction"])


def test_constructor(car_plate_object):
    assert car_plate_object.license_plates[0].value == "7EQE707"


def test__str__(car_plate_object):
    assert type(car_plate_object.__str__()) == str


def test_all_na(car_plate_object_all_na):
    assert len(car_plate_object_all_na.license_plates) == 0


def test_compare_1(car_plate_object):
    # Compare same object must return all True
    benchmark = CarPlate.compare(car_plate_object, car_plate_object)
    for value in benchmark.values():
        assert value is True


def test_compare_2(car_plate_object, car_plate_object_all_na):
    # Compare full object and empty object
    benchmark = CarPlate.compare(car_plate_object, car_plate_object_all_na)
    for value in benchmark.values():
        assert value is False


def test_compare_3(car_plate_object_from_scratch):
    # Compare car plates from class
    benchmark = CarPlate.compare(
        car_plate_object_from_scratch, car_plate_object_from_scratch
    )
    for key in benchmark.keys():
        if "__acc__" in key:
            assert benchmark[key] is True


def test_compare_4(car_plate_object_from_scratch):
    # Compare car plates from class with empty taxes
    car_plate_object_from_scratch.license_plates = []
    benchmark = CarPlate.compare(
        car_plate_object_from_scratch, car_plate_object_from_scratch
    )
    for key in benchmark.keys():
        if "__acc__" in key:
            assert benchmark[key] is True
        elif "__pre__" in key:
            assert benchmark[key] in [True, None]


def test_empty_object_works():
    car_plate = CarPlate()
    assert len(car_plate.license_plates) == 0
