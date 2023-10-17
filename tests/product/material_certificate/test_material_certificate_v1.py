import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product import MaterialCertificateV1
from mindee.product.material_certificate.material_certificate_v1_document import (
    MaterialCertificateV1Document,
)
from tests.product import PRODUCT_DATA_DIR


@pytest.fixture
def complete_doc() -> (
    Document[MaterialCertificateV1Document, Page[MaterialCertificateV1Document]]
):
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "material_certificate" / "response_v1" / "complete.json",
            encoding="utf-8",
        )
    )
    return Document(MaterialCertificateV1, json_data["document"])


@pytest.fixture
def empty_doc() -> (
    Document[MaterialCertificateV1Document, Page[MaterialCertificateV1Document]]
):
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "material_certificate" / "response_v1" / "empty.json",
            encoding="utf-8",
        )
    )
    return Document(MaterialCertificateV1, json_data["document"])


@pytest.fixture
def complete_page_0() -> Page[MaterialCertificateV1Document]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "material_certificate" / "response_v1" / "complete.json",
            encoding="utf-8",
        )
    )
    return Page(
        MaterialCertificateV1Document, json_data["document"]["inference"]["pages"][0]
    )


def test_complete_doc(
    complete_doc: Document[
        MaterialCertificateV1Document, Page[MaterialCertificateV1Document]
    ]
):
    reference_str = open(
        PRODUCT_DATA_DIR / "material_certificate" / "response_v1" / "summary_full.rst",
        "r",
        encoding="utf-8",
    ).read()
    assert str(complete_doc) == reference_str


def test_empty_doc(
    empty_doc: Document[
        MaterialCertificateV1Document, Page[MaterialCertificateV1Document]
    ]
):
    prediction = empty_doc.inference.prediction
    assert prediction.certificate_type.value is None
    assert prediction.norm.value is None
    assert prediction.heat_number.value is None
