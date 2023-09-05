import json

import pytest

from mindee.documents.fr import CarteGriseV1

FR_CARTE_GRISE_DATA_DIR = "./tests/data/products/carte_grise"
FILE_PATH_FR_CARTE_GRISE_V1_COMPLETE = (
    f"{FR_CARTE_GRISE_DATA_DIR}/response_v1/complete.json"
)
FILE_PATH_FR_CARTE_GRISE_V1_EMPTY = f"{FR_CARTE_GRISE_DATA_DIR}/response_v1/empty.json"


@pytest.fixture
def carte_grise_v1_doc_object() -> CarteGriseV1:
    json_data = json.load(open(FILE_PATH_FR_CARTE_GRISE_V1_COMPLETE))
    return CarteGriseV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def carte_grise_v1_doc_object_empty() -> CarteGriseV1:
    json_data = json.load(open(FILE_PATH_FR_CARTE_GRISE_V1_EMPTY))
    return CarteGriseV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def bank_check_pred():
    json_data = json.load(open(FILE_PATH_FR_CARTE_GRISE_V1_EMPTY))
    return json_data["document"]["inference"]["pages"][0]


# Technical tests
def test_constructor(carte_grise_v1_doc_object):
    assert carte_grise_v1_doc_object.formula_number.value == "2016AE00000"
    assert (
        carte_grise_v1_doc_object.mrz1.value
        == "CRFRADFXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXVP<<<<"
    )
    assert (
        carte_grise_v1_doc_object.mrz2.value
        == "CRFRADFXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXVP<<<<"
    )
    assert carte_grise_v1_doc_object.owner_first_name.value == "JOHN"
    assert carte_grise_v1_doc_object.owner_surname.value == "DOE"
    assert carte_grise_v1_doc_object.a.value == "DY-757-ZH"
    assert carte_grise_v1_doc_object.b.value == "2015-01-01"
    assert carte_grise_v1_doc_object.c1.value == "JOHN DOE"
    assert carte_grise_v1_doc_object.c3.value == "10 CHM PIOU 13540"
    assert carte_grise_v1_doc_object.c41.value == "2 JANE DOE"
    assert carte_grise_v1_doc_object.c4a.value == "EST LE PROPRIETAIRE DU VEHICULE"
    assert carte_grise_v1_doc_object.d1.value == "PEUGEOT"
    assert carte_grise_v1_doc_object.d3.value == "100"
    assert carte_grise_v1_doc_object.e.value == "VF000000000000000"
    assert carte_grise_v1_doc_object.f1.value == "1100"
    assert carte_grise_v1_doc_object.f2.value == "1600"
    assert carte_grise_v1_doc_object.f3.value == "1600"
    assert carte_grise_v1_doc_object.g.value == "12"
    assert carte_grise_v1_doc_object.g1.value == "1115"
    assert carte_grise_v1_doc_object.i.value == "2016-01-19"
    assert carte_grise_v1_doc_object.j.value == "M1"
    assert carte_grise_v1_doc_object.j1.value == "VP"
    assert carte_grise_v1_doc_object.j2.value == "123"
    assert carte_grise_v1_doc_object.j3.value == "CI"
    assert carte_grise_v1_doc_object.p1.value == "1761"
    assert carte_grise_v1_doc_object.p2.value == "11"
    assert carte_grise_v1_doc_object.p3.value == "ES"
    assert carte_grise_v1_doc_object.p6.value == "7"
    assert carte_grise_v1_doc_object.q.value == ""
    assert carte_grise_v1_doc_object.s1.value == "5"
    assert carte_grise_v1_doc_object.s2.value == ""
    assert carte_grise_v1_doc_object.u1.value == "33"
    assert carte_grise_v1_doc_object.u2.value == "6125"
    assert carte_grise_v1_doc_object.v7.value == "198"
    assert carte_grise_v1_doc_object.x1.value == "2018-01-04"
    assert carte_grise_v1_doc_object.y1.value == "179"
    assert carte_grise_v1_doc_object.y2.value == "0"
    assert carte_grise_v1_doc_object.y3.value == "0"
    assert carte_grise_v1_doc_object.y4.value == "4"
    assert carte_grise_v1_doc_object.y5.value == "2.76"
    assert carte_grise_v1_doc_object.y6.value == "185.76"
    doc_str = (
        open(f"{FR_CARTE_GRISE_DATA_DIR}/response_v1/doc_to_string.txt").read().strip()
    )
    print(str(carte_grise_v1_doc_object))
    assert str(carte_grise_v1_doc_object) == doc_str


def test_all_na(carte_grise_v1_doc_object_empty):
    assert carte_grise_v1_doc_object_empty.formula_number.value is None
    assert carte_grise_v1_doc_object_empty.mrz1.value is None
    assert carte_grise_v1_doc_object_empty.mrz2.value is None
    assert carte_grise_v1_doc_object_empty.owner_first_name.value is None
    assert carte_grise_v1_doc_object_empty.owner_surname.value is None
    assert carte_grise_v1_doc_object_empty.a.value is None
    assert carte_grise_v1_doc_object_empty.b.value is None
    assert carte_grise_v1_doc_object_empty.c1.value is None
    assert carte_grise_v1_doc_object_empty.c3.value is None
    assert carte_grise_v1_doc_object_empty.c41.value is None
    assert carte_grise_v1_doc_object_empty.c4a.value is None
    assert carte_grise_v1_doc_object_empty.d1.value is None
    assert carte_grise_v1_doc_object_empty.d3.value is None
    assert carte_grise_v1_doc_object_empty.e.value is None
    assert carte_grise_v1_doc_object_empty.f1.value is None
    assert carte_grise_v1_doc_object_empty.f2.value is None
    assert carte_grise_v1_doc_object_empty.f3.value is None
    assert carte_grise_v1_doc_object_empty.g.value is None
    assert carte_grise_v1_doc_object_empty.g1.value is None
    assert carte_grise_v1_doc_object_empty.i.value is None
    assert carte_grise_v1_doc_object_empty.j.value is None
    assert carte_grise_v1_doc_object_empty.j1.value is None
    assert carte_grise_v1_doc_object_empty.j2.value is None
    assert carte_grise_v1_doc_object_empty.j3.value is None
    assert carte_grise_v1_doc_object_empty.p1.value is None
    assert carte_grise_v1_doc_object_empty.p2.value is None
    assert carte_grise_v1_doc_object_empty.p3.value is None
    assert carte_grise_v1_doc_object_empty.p6.value is None
    assert carte_grise_v1_doc_object_empty.q.value is None
    assert carte_grise_v1_doc_object_empty.s1.value is None
    assert carte_grise_v1_doc_object_empty.s2.value is None
    assert carte_grise_v1_doc_object_empty.u1.value is None
    assert carte_grise_v1_doc_object_empty.u2.value is None
    assert carte_grise_v1_doc_object_empty.v7.value is None
    assert carte_grise_v1_doc_object_empty.x1.value is None
    assert carte_grise_v1_doc_object_empty.y1.value is None
    assert carte_grise_v1_doc_object_empty.y2.value is None
    assert carte_grise_v1_doc_object_empty.y3.value is None
    assert carte_grise_v1_doc_object_empty.y4.value is None
    assert carte_grise_v1_doc_object_empty.y5.value is None
    assert carte_grise_v1_doc_object_empty.y6.value is None
