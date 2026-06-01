import pytest

from mindee.v1.client import Client
from mindee.v1.product.international_id import InternationalIdV2
from mindee.v1.product.invoice.invoice_v4 import InvoiceV4
from tests.utils import V1_PRODUCT_DATA_DIR


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.mark.integration
def test_send_cropper_extra(client):
    sample = client.source_from_path(
        V1_PRODUCT_DATA_DIR / "invoices" / "default_sample.jpg",
    )
    response = client.parse(InvoiceV4, sample, cropper=True)
    assert response.document.inference.pages[0].extras.cropper


@pytest.mark.integration
def test_send_full_text_ocr_extra(client):
    sample = client.source_from_path(
        V1_PRODUCT_DATA_DIR / "international_id" / "default_sample.jpg",
    )
    response = client.enqueue_and_parse(InternationalIdV2, sample, full_text=True)
    assert response.document.extras.full_text_ocr
