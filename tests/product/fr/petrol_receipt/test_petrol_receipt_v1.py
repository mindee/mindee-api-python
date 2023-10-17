import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.fr import PetrolReceiptV1
from mindee.product.fr.petrol_receipt.petrol_receipt_v1_document import (
    PetrolReceiptV1Document,
)
from tests.product import PRODUCT_DATA_DIR


@pytest.fixture
def complete_doc() -> Document[PetrolReceiptV1Document, Page[PetrolReceiptV1Document]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "petrol_receipts" / "response_v1" / "complete.json",
            encoding="utf-8",
        )
    )
    return Document(PetrolReceiptV1, json_data["document"])


@pytest.fixture
def empty_doc() -> Document[PetrolReceiptV1Document, Page[PetrolReceiptV1Document]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "petrol_receipts" / "response_v1" / "empty.json",
            encoding="utf-8",
        )
    )
    return Document(PetrolReceiptV1, json_data["document"])


@pytest.fixture
def complete_page_0() -> Page[PetrolReceiptV1Document]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "petrol_receipts" / "response_v1" / "complete.json",
            encoding="utf-8",
        )
    )
    return Page(PetrolReceiptV1Document, json_data["document"]["inference"]["pages"][0])


def test_complete_doc(
    complete_doc: Document[PetrolReceiptV1Document, Page[PetrolReceiptV1Document]]
):
    reference_str = open(
        PRODUCT_DATA_DIR / "petrol_receipts" / "response_v1" / "summary_full.rst",
        "r",
        encoding="utf-8",
    ).read()
    assert str(complete_doc) == reference_str


def test_empty_doc(
    empty_doc: Document[PetrolReceiptV1Document, Page[PetrolReceiptV1Document]]
):
    prediction = empty_doc.inference.prediction
    assert prediction.fuel.category is None
    assert prediction.fuel.raw_text is None
    assert prediction.price.value is None
    assert prediction.volume.value is None
    assert prediction.total.amount is None


def test_complete_page_0(complete_page_0: Page[PetrolReceiptV1Document]):
    reference_str = open(
        PRODUCT_DATA_DIR / "petrol_receipts" / "response_v1" / "summary_page0.rst",
        "r",
        encoding="utf-8",
    ).read()
    assert complete_page_0.id == 0
    assert str(complete_page_0) == reference_str
