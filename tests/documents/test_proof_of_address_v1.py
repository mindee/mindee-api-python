import json

import pytest

from mindee.documents.proof_of_address.proof_of_address_v1 import ProofOfAddressV1
from tests import PROOF_OF_ADDRESS_DATA_DIR

FILE_PATH_PROOF_OF_ADDRESS_V1_COMPLETE = (
    f"{PROOF_OF_ADDRESS_DATA_DIR}/response_v1/complete.json"
)


@pytest.fixture
def proof_of_address_v1_doc_object() -> ProofOfAddressV1:
    json_data = json.load(open(FILE_PATH_PROOF_OF_ADDRESS_V1_COMPLETE))
    return ProofOfAddressV1(
        api_prediction=json_data["document"]["inference"], page_n=None
    )


@pytest.fixture
def proof_of_address_v1_doc_object_empty() -> ProofOfAddressV1:
    json_data = json.load(open(f"{PROOF_OF_ADDRESS_DATA_DIR}/response_v1/empty.json"))
    return ProofOfAddressV1(
        api_prediction=json_data["document"]["inference"], page_n=None
    )


@pytest.fixture
def proof_of_address_v1_page_object() -> ProofOfAddressV1:
    json_data = json.load(open(FILE_PATH_PROOF_OF_ADDRESS_V1_COMPLETE))
    return ProofOfAddressV1(
        api_prediction=json_data["document"]["inference"]["pages"][0], page_n=0
    )


def test_doc_constructor(proof_of_address_v1_doc_object):
    doc_str = (
        open(f"{PROOF_OF_ADDRESS_DATA_DIR}/response_v1/doc_to_string.txt")
        .read()
        .strip()
    )
    assert proof_of_address_v1_doc_object.issuer_name.page_n == 0
    assert str(proof_of_address_v1_doc_object) == doc_str


def test_page_constructor(proof_of_address_v1_page_object):
    doc_str = (
        open(f"{PROOF_OF_ADDRESS_DATA_DIR}/response_v1/page0_to_string.txt")
        .read()
        .strip()
    )
    assert proof_of_address_v1_page_object.orientation.value == 0
    assert proof_of_address_v1_page_object.issuer_name.page_n == 0
    assert str(proof_of_address_v1_page_object) == doc_str
    assert len(proof_of_address_v1_page_object.cropper) == 0


def test_all_na(proof_of_address_v1_doc_object_empty):
    assert proof_of_address_v1_doc_object_empty.locale.value is None
    assert proof_of_address_v1_doc_object_empty.date.value is None
    assert len(proof_of_address_v1_doc_object_empty.dates) == 0
    assert proof_of_address_v1_doc_object_empty.issuer_address.value is None
    assert len(proof_of_address_v1_doc_object_empty.issuer_company_registration) == 0
    assert proof_of_address_v1_doc_object_empty.issuer_name.value is None
    assert proof_of_address_v1_doc_object_empty.recipient_address.value is None
    assert len(proof_of_address_v1_doc_object_empty.recipient_company_registration) == 0
    assert proof_of_address_v1_doc_object_empty.recipient_name.value is None
