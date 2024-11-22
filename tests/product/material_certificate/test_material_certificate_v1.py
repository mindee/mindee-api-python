import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.material_certificate.material_certificate_v1 import (
    MaterialCertificateV1,
)
from mindee.product.material_certificate.material_certificate_v1_document import (
    MaterialCertificateV1Document,
)
from tests.product import PRODUCT_DATA_DIR

RESPONSE_DIR = PRODUCT_DATA_DIR / "material_certificate" / "response_v1"

MaterialCertificateV1DocumentType = Document[
    MaterialCertificateV1Document,
    Page[MaterialCertificateV1Document],
]


@pytest.fixture
def complete_doc() -> MaterialCertificateV1DocumentType:
    file_path = RESPONSE_DIR / "complete.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(MaterialCertificateV1, json_data["document"])


@pytest.fixture
def empty_doc() -> MaterialCertificateV1DocumentType:
    file_path = RESPONSE_DIR / "empty.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(MaterialCertificateV1, json_data["document"])


def test_complete_doc(complete_doc: MaterialCertificateV1DocumentType):
    file_path = RESPONSE_DIR / "summary_full.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: MaterialCertificateV1DocumentType):
    prediction = empty_doc.inference.prediction
    assert prediction.certificate_type.value is None
    assert prediction.norm.value is None
    assert prediction.heat_number.value is None
