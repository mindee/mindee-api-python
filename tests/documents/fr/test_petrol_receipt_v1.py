import json

import pytest

from mindee.documents.fr import PetrolReceiptV1

FR_PETROL_RECEIPT_DATA_DIR = "./tests/data/products/petrol_receipts"
FILE_PATH_FR_PETROL_RECEIPT_V1_COMPLETE = (
    f"{ FR_PETROL_RECEIPT_DATA_DIR }/response_v1/complete.json"
)
FILE_PATH_FR_PETROL_RECEIPT_V1_EMPTY = (
    f"{ FR_PETROL_RECEIPT_DATA_DIR }/response_v1/empty.json"
)


@pytest.fixture
def petrol_receipt_v1_doc() -> PetrolReceiptV1:
    json_data = json.load(
        open(FILE_PATH_FR_PETROL_RECEIPT_V1_COMPLETE, encoding="utf-8"),
    )
    return PetrolReceiptV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def petrol_receipt_v1_doc_empty() -> PetrolReceiptV1:
    json_data = json.load(
        open(FILE_PATH_FR_PETROL_RECEIPT_V1_EMPTY, encoding="utf-8"),
    )
    return PetrolReceiptV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def petrol_receipt_v1_page0():
    json_data = json.load(
        open(FILE_PATH_FR_PETROL_RECEIPT_V1_COMPLETE, encoding="utf-8"),
    )
    return PetrolReceiptV1(json_data["document"]["inference"]["pages"][0], page_n=0)


def test_empty_doc_constructor(petrol_receipt_v1_doc_empty):
    assert petrol_receipt_v1_doc_empty.fuel.category is None
    assert petrol_receipt_v1_doc_empty.fuel.raw_text is None
    assert petrol_receipt_v1_doc_empty.price.value is None
    assert petrol_receipt_v1_doc_empty.volume.value is None
    assert petrol_receipt_v1_doc_empty.total.amount is None
