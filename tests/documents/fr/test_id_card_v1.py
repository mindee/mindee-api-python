import json

import pytest

from mindee.documents.fr import IdCardV1

FR_ID_CARD_DATA_DIR = "./tests/data/products/idcard_fr"
FILE_PATH_FR_ID_CARD_V1_COMPLETE = f"{ FR_ID_CARD_DATA_DIR }/response_v1/complete.json"
FILE_PATH_FR_ID_CARD_V1_EMPTY = f"{ FR_ID_CARD_DATA_DIR }/response_v1/empty.json"


@pytest.fixture
def id_card_v1_doc() -> IdCardV1:
    json_data = json.load(open(FILE_PATH_FR_ID_CARD_V1_COMPLETE))
    return IdCardV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def id_card_v1_doc_empty() -> IdCardV1:
    json_data = json.load(open(FILE_PATH_FR_ID_CARD_V1_EMPTY))
    return IdCardV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def id_card_v1_page0():
    json_data = json.load(open(FILE_PATH_FR_ID_CARD_V1_COMPLETE))
    return IdCardV1(json_data["document"]["inference"]["pages"][0], page_n=0)


def test_empty_doc_constructor(id_card_v1_doc_empty):
    assert id_card_v1_doc_empty.id_number.value is None
    assert len(id_card_v1_doc_empty.given_names) == 0
    assert id_card_v1_doc_empty.surname.value is None
    assert id_card_v1_doc_empty.birth_date.value is None
    assert id_card_v1_doc_empty.birth_place.value is None
    assert id_card_v1_doc_empty.expiry_date.value is None
    assert id_card_v1_doc_empty.authority.value is None
    assert id_card_v1_doc_empty.gender.value is None
    assert id_card_v1_doc_empty.mrz1.value is None
    assert id_card_v1_doc_empty.mrz2.value is None


def test_doc_constructor(id_card_v1_doc):
    file_path = f"{ FR_ID_CARD_DATA_DIR }/response_v1/doc_to_string.rst"
    reference_str = open(file_path, "r", encoding="utf-8").read()
    assert str(id_card_v1_doc) == reference_str


def test_page0_constructor(id_card_v1_page0):
    file_path = f"{ FR_ID_CARD_DATA_DIR }/response_v1/page0_to_string.rst"
    reference_str = open(file_path, "r", encoding="utf-8").read()
    assert str(id_card_v1_page0) == reference_str
