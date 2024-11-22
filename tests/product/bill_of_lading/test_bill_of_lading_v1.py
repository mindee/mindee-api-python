import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.bill_of_lading.bill_of_lading_v1 import BillOfLadingV1
from mindee.product.bill_of_lading.bill_of_lading_v1_document import (
    BillOfLadingV1Document,
)
from tests.product import PRODUCT_DATA_DIR

RESPONSE_DIR = PRODUCT_DATA_DIR / "bill_of_lading" / "response_v1"

BillOfLadingV1DocumentType = Document[
    BillOfLadingV1Document,
    Page[BillOfLadingV1Document],
]


@pytest.fixture
def complete_doc() -> BillOfLadingV1DocumentType:
    file_path = RESPONSE_DIR / "complete.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(BillOfLadingV1, json_data["document"])


@pytest.fixture
def empty_doc() -> BillOfLadingV1DocumentType:
    file_path = RESPONSE_DIR / "empty.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(BillOfLadingV1, json_data["document"])


def test_complete_doc(complete_doc: BillOfLadingV1DocumentType):
    file_path = RESPONSE_DIR / "summary_full.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: BillOfLadingV1DocumentType):
    prediction = empty_doc.inference.prediction
    assert prediction.bill_of_lading_number.value is None
    assert prediction.shipper.address is None
    assert prediction.shipper.email is None
    assert prediction.shipper.name is None
    assert prediction.shipper.phone is None
    assert prediction.consignee.address is None
    assert prediction.consignee.email is None
    assert prediction.consignee.name is None
    assert prediction.consignee.phone is None
    assert prediction.notify_party.address is None
    assert prediction.notify_party.email is None
    assert prediction.notify_party.name is None
    assert prediction.notify_party.phone is None
    assert prediction.carrier.name is None
    assert prediction.carrier.professional_number is None
    assert prediction.carrier.scac is None
    assert len(prediction.carrier_items) == 0
    assert prediction.port_of_loading.value is None
    assert prediction.port_of_discharge.value is None
    assert prediction.place_of_delivery.value is None
    assert prediction.date_of_issue.value is None
    assert prediction.departure_date.value is None
