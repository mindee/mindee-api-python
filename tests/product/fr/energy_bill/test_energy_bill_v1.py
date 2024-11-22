import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.fr.energy_bill.energy_bill_v1 import EnergyBillV1
from mindee.product.fr.energy_bill.energy_bill_v1_document import (
    EnergyBillV1Document,
)
from tests.product import PRODUCT_DATA_DIR

RESPONSE_DIR = PRODUCT_DATA_DIR / "energy_bill_fra" / "response_v1"

EnergyBillV1DocumentType = Document[
    EnergyBillV1Document,
    Page[EnergyBillV1Document],
]


@pytest.fixture
def complete_doc() -> EnergyBillV1DocumentType:
    file_path = RESPONSE_DIR / "complete.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(EnergyBillV1, json_data["document"])


@pytest.fixture
def empty_doc() -> EnergyBillV1DocumentType:
    file_path = RESPONSE_DIR / "empty.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(EnergyBillV1, json_data["document"])


def test_complete_doc(complete_doc: EnergyBillV1DocumentType):
    file_path = RESPONSE_DIR / "summary_full.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: EnergyBillV1DocumentType):
    prediction = empty_doc.inference.prediction
    assert prediction.invoice_number.value is None
    assert prediction.contract_id.value is None
    assert prediction.delivery_point.value is None
    assert prediction.invoice_date.value is None
    assert prediction.due_date.value is None
    assert prediction.total_before_taxes.value is None
    assert prediction.total_taxes.value is None
    assert prediction.total_amount.value is None
    assert prediction.energy_supplier.address is None
    assert prediction.energy_supplier.name is None
    assert prediction.energy_consumer.address is None
    assert prediction.energy_consumer.name is None
    assert len(prediction.subscription) == 0
    assert len(prediction.energy_usage) == 0
    assert len(prediction.taxes_and_contributions) == 0
    assert prediction.meter_details.meter_number is None
    assert prediction.meter_details.meter_type is None
    assert prediction.meter_details.unit is None
