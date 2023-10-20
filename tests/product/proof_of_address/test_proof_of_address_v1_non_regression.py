from mindee.client import Client

from mindee.product import ProofOfAddressV1
from tests.product import PRODUCT_DATA_DIR, get_id, get_version


def test_default_sample():
    client = Client()
    with open(
        PRODUCT_DATA_DIR / "proof_of_address" / "response_v1" / "default_sample.rst",
        encoding="utf-8",
    ) as rst_file:
        rst_ref = rst_file.read()

    sample = client.source_from_path(
        PRODUCT_DATA_DIR / "proof_of_address" / "default_sample.jpg"
    )
    response = client.parse(ProofOfAddressV1, sample)
    doc_response = response.document
    doc_response.id = get_id(rst_ref)
    doc_response.inference.product.version = get_version(rst_ref)
    assert str(doc_response) == rst_ref
