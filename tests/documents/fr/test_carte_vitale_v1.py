import json

import pytest

from mindee.documents.fr import CarteVitaleV1

FR_CARTE_VITALE_DATA_DIR = "./tests/data/fr/carte_vitale"

FILE_PATH_FR_CARTE_VITALE_V1_COMPLETE = (
    f"{ FR_CARTE_VITALE_DATA_DIR }/response_v1/complete.json"
)
FILE_PATH_FR_CARTE_VITALE_V1_EMPTY = (
    f"{ FR_CARTE_VITALE_DATA_DIR }/response_v1/empty.json"
)


@pytest.fixture
def carte_vitale_v1_doc() -> CarteVitaleV1:
    json_data = json.load(open(FILE_PATH_FR_CARTE_VITALE_V1_COMPLETE))
    return CarteVitaleV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def carte_vitale_v1_doc_empty() -> CarteVitaleV1:
    json_data = json.load(open(FILE_PATH_FR_CARTE_VITALE_V1_EMPTY))
    return CarteVitaleV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def carte_vitale_v1_page0():
    json_data = json.load(open(FILE_PATH_FR_CARTE_VITALE_V1_COMPLETE))
    return CarteVitaleV1(json_data["document"]["inference"]["pages"][0], page_n=0)


def test_doc_constructor(carte_vitale_v1_doc):
    file_path = f"{ FR_CARTE_VITALE_DATA_DIR }/response_v1/doc_to_string.txt"
    reference_str = open(file_path, "r", encoding="utf-8").read().strip()
    assert str(carte_vitale_v1_doc) == reference_str


def test_page0_constructor(carte_vitale_v1_page0):
    file_path = f"{ FR_CARTE_VITALE_DATA_DIR }/response_v1/page0_to_string.txt"
    reference_str = open(file_path, "r", encoding="utf-8").read().strip()
    assert str(carte_vitale_v1_page0) == reference_str
