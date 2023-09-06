import json

import pytest

from mindee.documents import ProofOfAddressV1

PROOF_OF_ADDRESS_DATA_DIR = "./tests/data/products/proof_of_address"
FILE_PATH_PROOF_OF_ADDRESS_V1_COMPLETE = (
    f"{ PROOF_OF_ADDRESS_DATA_DIR }/response_v1/complete.json"
)
FILE_PATH_PROOF_OF_ADDRESS_V1_EMPTY = (
    f"{ PROOF_OF_ADDRESS_DATA_DIR }/response_v1/empty.json"
)


@pytest.fixture
def proof_of_address_v1_doc() -> ProofOfAddressV1:
    json_data = json.load(open(FILE_PATH_PROOF_OF_ADDRESS_V1_COMPLETE))
    return ProofOfAddressV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def proof_of_address_v1_doc_empty() -> ProofOfAddressV1:
    json_data = json.load(open(FILE_PATH_PROOF_OF_ADDRESS_V1_EMPTY))
    return ProofOfAddressV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def proof_of_address_v1_page0():
    json_data = json.load(open(FILE_PATH_PROOF_OF_ADDRESS_V1_COMPLETE))
    return ProofOfAddressV1(json_data["document"]["inference"]["pages"][0], page_n=0)


def test_empty_doc_constructor(proof_of_address_v1_doc_empty):
    assert proof_of_address_v1_doc_empty.locale.value is None
    assert proof_of_address_v1_doc_empty.issuer_name.value is None
    assert len(proof_of_address_v1_doc_empty.issuer_company_registration) == 0
    assert proof_of_address_v1_doc_empty.issuer_address.value is None
    assert proof_of_address_v1_doc_empty.recipient_name.value is None
    assert len(proof_of_address_v1_doc_empty.recipient_company_registration) == 0
    assert proof_of_address_v1_doc_empty.recipient_address.value is None
    assert len(proof_of_address_v1_doc_empty.dates) == 0
    assert proof_of_address_v1_doc_empty.date.value is None


def test_doc_constructor(proof_of_address_v1_doc):
    file_path = f"{ PROOF_OF_ADDRESS_DATA_DIR }/response_v1/doc_to_string.rst"
    reference_str = open(file_path, "r", encoding="utf-8").read()
    assert str(proof_of_address_v1_doc) == reference_str


def test_page0_constructor(proof_of_address_v1_page0):
    file_path = f"{ PROOF_OF_ADDRESS_DATA_DIR }/response_v1/page0_to_string.rst"
    reference_str = open(file_path, "r", encoding="utf-8").read()
    assert str(proof_of_address_v1_page0) == reference_str
