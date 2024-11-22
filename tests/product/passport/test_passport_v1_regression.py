import pytest

from mindee.client import Client
from mindee.product.passport.passport_v1 import PassportV1
from tests.product import PRODUCT_DATA_DIR, get_id, get_version


@pytest.mark.regression
def test_default_sample():
    client = Client()
    with open(
        PRODUCT_DATA_DIR / "passport" / "response_v1" / "default_sample.rst",
        encoding="utf-8",
    ) as rst_file:
        rst_ref = rst_file.read()

    sample = client.source_from_path(
        PRODUCT_DATA_DIR / "passport" / "default_sample.jpg",
    )
    response = client.parse(PassportV1, sample)
    doc_response = response.document
    doc_response.id = get_id(rst_ref)
    doc_response.inference.product.version = get_version(rst_ref)
    assert str(doc_response) == rst_ref
