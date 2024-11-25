import pytest

from mindee.client import Client
from mindee.product.fr.carte_grise.carte_grise_v1 import CarteGriseV1
from tests.product import PRODUCT_DATA_DIR, get_id, get_version


@pytest.mark.regression
def test_default_sample():
    client = Client()
    with open(
        PRODUCT_DATA_DIR / "carte_grise" / "response_v1" / "default_sample.rst",
        encoding="utf-8",
    ) as rst_file:
        rst_ref = rst_file.read()

    sample = client.source_from_path(
        PRODUCT_DATA_DIR / "carte_grise" / "default_sample.jpg",
    )
    response = client.parse(CarteGriseV1, sample)
    doc_response = response.document
    doc_response.id = get_id(rst_ref)
    doc_response.inference.product.version = get_version(rst_ref)
    assert str(doc_response) == rst_ref
