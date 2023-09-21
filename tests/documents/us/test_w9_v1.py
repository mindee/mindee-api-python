import json

import pytest

from mindee.documents.us import W9V1

US_W9_DATA_DIR = "./tests/data/products/us_w9"
FILE_PATH_US_W9_V1_COMPLETE = f"{ US_W9_DATA_DIR }/response_v1/complete.json"
FILE_PATH_US_W9_V1_EMPTY = f"{ US_W9_DATA_DIR }/response_v1/empty.json"


@pytest.fixture
def w9_v1_doc() -> W9V1:
    json_data = json.load(open(FILE_PATH_US_W9_V1_COMPLETE, encoding="utf-8"))
    return W9V1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def w9_v1_doc_empty() -> W9V1:
    json_data = json.load(open(FILE_PATH_US_W9_V1_EMPTY, encoding="utf-8"))
    return W9V1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def w9_v1_page0():
    json_data = json.load(open(FILE_PATH_US_W9_V1_COMPLETE, encoding="utf-8"))
    return W9V1(json_data["document"]["inference"]["pages"][0], page_n=0)


def test_empty_doc_constructor(w9_v1_doc_empty):
    assert w9_v1_doc_empty.name.value is None
    assert w9_v1_doc_empty.ssn.value is None
    assert w9_v1_doc_empty.address.value is None
    assert w9_v1_doc_empty.city_state_zip.value is None
    assert w9_v1_doc_empty.business_name.value is None
    assert w9_v1_doc_empty.ein.value is None
    assert w9_v1_doc_empty.tax_classification.value is None
    assert w9_v1_doc_empty.tax_classification_other_details.value is None
    assert w9_v1_doc_empty.w9_revision_date.value is None
    assert w9_v1_doc_empty.signature_position.value is None
    assert w9_v1_doc_empty.signature_date_position.value is None
    assert w9_v1_doc_empty.tax_classification_llc.value is None
