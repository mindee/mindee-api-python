import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product import ProofOfAddressV1
from mindee.product.proof_of_address.proof_of_address_v1_document import (
    ProofOfAddressV1Document,
)
from tests.product import PRODUCT_DATA_DIR

RESPONSE_DIR = PRODUCT_DATA_DIR / "proof_of_address" / "response_v1"

ProofOfAddressV1DocumentType = Document[
    ProofOfAddressV1Document,
    Page[ProofOfAddressV1Document],
]


@pytest.fixture
def complete_doc() -> ProofOfAddressV1DocumentType:
    file_path = RESPONSE_DIR / "complete.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(ProofOfAddressV1, json_data["document"])


@pytest.fixture
def empty_doc() -> ProofOfAddressV1DocumentType:
    file_path = RESPONSE_DIR / "empty.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(ProofOfAddressV1, json_data["document"])


def test_complete_doc(complete_doc: ProofOfAddressV1DocumentType):
    file_path = RESPONSE_DIR / "summary_full.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: ProofOfAddressV1DocumentType):
    prediction = empty_doc.inference.prediction
    assert prediction.locale.value is None
    assert prediction.issuer_name.value is None
    assert len(prediction.issuer_company_registration) == 0
    assert prediction.issuer_address.value is None
    assert prediction.recipient_name.value is None
    assert len(prediction.recipient_company_registration) == 0
    assert prediction.recipient_address.value is None
    assert len(prediction.dates) == 0
    assert prediction.date.value is None
