import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product import ProofOfAddressV1
from mindee.product.proof_of_address.proof_of_address_v1_document import (
    ProofOfAddressV1Document,
)
from tests.product import PRODUCT_DATA_DIR


@pytest.fixture
def complete_doc() -> (
    Document[ProofOfAddressV1Document, Page[ProofOfAddressV1Document]]
):
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "proof_of_address" / "response_v1" / "complete.json",
            encoding="utf-8",
        )
    )
    return Document(ProofOfAddressV1, json_data["document"])


@pytest.fixture
def empty_doc() -> Document[ProofOfAddressV1Document, Page[ProofOfAddressV1Document]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "proof_of_address" / "response_v1" / "empty.json",
            encoding="utf-8",
        )
    )
    return Document(ProofOfAddressV1, json_data["document"])


@pytest.fixture
def complete_page_0() -> Page[ProofOfAddressV1Document]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "proof_of_address" / "response_v1" / "complete.json",
            encoding="utf-8",
        )
    )
    return Page(
        ProofOfAddressV1Document, json_data["document"]["inference"]["pages"][0]
    )


def test_complete_doc(
    complete_doc: Document[ProofOfAddressV1Document, Page[ProofOfAddressV1Document]]
):
    reference_str = open(
        PRODUCT_DATA_DIR / "proof_of_address" / "response_v1" / "summary_full.rst",
        "r",
        encoding="utf-8",
    ).read()
    assert str(complete_doc) == reference_str


def test_empty_doc(
    empty_doc: Document[ProofOfAddressV1Document, Page[ProofOfAddressV1Document]]
):
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
