import json

import pytest

from mindee.documents.eu.license_plate.license_plate_v1 import LicensePlateV1

EU_LICENSE_PLATE_DATA_DIR = "./tests/data/eu/license_plate"

FILE_PATH_EU_LICENSE_PLATE_V1_COMPLETE = (
    f"{ EU_LICENSE_PLATE_DATA_DIR }/response_v1/complete.json"
)
FILE_PATH_EU_LICENSE_PLATE_V1_EMPTY = (
    f"{ EU_LICENSE_PLATE_DATA_DIR }/response_v1/empty.json"
)


@pytest.fixture
def license_plate_v1_doc() -> LicensePlateV1:
    json_data = json.load(open(FILE_PATH_EU_LICENSE_PLATE_V1_COMPLETE))
    return LicensePlateV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def license_plate_v1_doc_empty() -> LicensePlateV1:
    json_data = json.load(open(FILE_PATH_EU_LICENSE_PLATE_V1_EMPTY))
    return LicensePlateV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def license_plate_v1_page0():
    json_data = json.load(open(FILE_PATH_EU_LICENSE_PLATE_V1_COMPLETE))
    return LicensePlateV1(json_data["document"]["inference"]["pages"][0], page_n=0)


def test_doc_constructor(license_plate_v1_doc):
    file_path = f"{ EU_LICENSE_PLATE_DATA_DIR }/response_v1/doc_to_string.txt"
    reference_str = open(file_path, "r", encoding="utf-8").read().strip()
    assert str(license_plate_v1_doc) == reference_str


def test_page0_constructor(license_plate_v1_page0):
    file_path = f"{ EU_LICENSE_PLATE_DATA_DIR }/response_v1/page0_to_string.txt"
    reference_str = open(file_path, "r", encoding="utf-8").read().strip()
    assert str(license_plate_v1_page0) == reference_str
