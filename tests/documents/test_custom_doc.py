import json

import pytest

from mindee.documents.custom_document import CustomDocument
from tests import CUSTOM_DATA_DIR

CUSTOM_FILE_PATH = f"{CUSTOM_DATA_DIR}/response/complete.json"
CUSTOM_NA_FILE_PATH = f"{CUSTOM_DATA_DIR}/response/empty.json"


@pytest.fixture
def custom_doc_object():
    json_data = json.load(open(CUSTOM_FILE_PATH))
    return CustomDocument(
        "field_test", json_data["document"]["inference"]["prediction"], page_n=None
    )


@pytest.fixture
def invoice_pred():
    json_data = json.load(open(CUSTOM_NA_FILE_PATH))
    return json_data["document"]["inference"]["pages"][0]["prediction"]


@pytest.fixture
def custom_doc_object_all_na(invoice_pred):
    return CustomDocument("field_test", invoice_pred)


def test_constructor(custom_doc_object):
    doc_str = open(f"{CUSTOM_DATA_DIR}/response/doc_to_string.txt").read().strip()
    assert str(custom_doc_object) == doc_str
