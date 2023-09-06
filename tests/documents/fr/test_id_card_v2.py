import json

import pytest

from mindee.documents.fr import IdCardV2

FR_ID_CARD_DATA_DIR = "./tests/data/products/idcard_fr"
FILE_PATH_FR_ID_CARD_V2_COMPLETE = f"{ FR_ID_CARD_DATA_DIR }/response_v2/complete.json"
FILE_PATH_FR_ID_CARD_V2_EMPTY = f"{ FR_ID_CARD_DATA_DIR }/response_v2/empty.json"


@pytest.fixture
def id_card_v2_doc() -> IdCardV2:
    json_data = json.load(open(FILE_PATH_FR_ID_CARD_V2_COMPLETE, encoding="utf-8"))
    return IdCardV2(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def id_card_v2_doc_empty() -> IdCardV2:
    json_data = json.load(open(FILE_PATH_FR_ID_CARD_V2_EMPTY, encoding="utf-8"))
    return IdCardV2(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def id_card_v2_page0():
    json_data = json.load(open(FILE_PATH_FR_ID_CARD_V2_COMPLETE, encoding="utf-8"))
    return IdCardV2(json_data["document"]["inference"]["pages"][0], page_n=0)


def test_empty_doc_constructor(id_card_v2_doc_empty):
    assert id_card_v2_doc_empty.nationality.value is None
    assert id_card_v2_doc_empty.card_access_number.value is None
    assert id_card_v2_doc_empty.document_number.value is None
    assert len(id_card_v2_doc_empty.given_names) == 0
    assert id_card_v2_doc_empty.surname.value is None
    assert id_card_v2_doc_empty.alternate_name.value is None
    assert id_card_v2_doc_empty.birth_date.value is None
    assert id_card_v2_doc_empty.birth_place.value is None
    assert id_card_v2_doc_empty.gender.value is None
    assert id_card_v2_doc_empty.expiry_date.value is None
    assert id_card_v2_doc_empty.mrz1.value is None
    assert id_card_v2_doc_empty.mrz2.value is None
    assert id_card_v2_doc_empty.mrz3.value is None
    assert id_card_v2_doc_empty.issue_date.value is None
    assert id_card_v2_doc_empty.authority.value is None


def test_doc_constructor(id_card_v2_doc):
    file_path = f"{ FR_ID_CARD_DATA_DIR }/response_v2/doc_to_string.rst"
    reference_str = open(file_path, "r", encoding="utf-8").read()
    assert str(id_card_v2_doc) == reference_str


def test_page0_constructor(id_card_v2_page0):
    file_path = f"{ FR_ID_CARD_DATA_DIR }/response_v2/page0_to_string.rst"
    reference_str = open(file_path, "r", encoding="utf-8").read()
    assert str(id_card_v2_page0) == reference_str
