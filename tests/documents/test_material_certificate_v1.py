import json

import pytest

from mindee.documents import MaterialCertificateV1

MATERIAL_CERTIFICATE_DATA_DIR = "./tests/data/products/material_certificate"
FILE_PATH_MATERIAL_CERTIFICATE_V1_COMPLETE = (
    f"{ MATERIAL_CERTIFICATE_DATA_DIR }/response_v1/complete.json"
)
FILE_PATH_MATERIAL_CERTIFICATE_V1_EMPTY = (
    f"{ MATERIAL_CERTIFICATE_DATA_DIR }/response_v1/empty.json"
)


@pytest.fixture
def material_certificate_v1_doc() -> MaterialCertificateV1:
    json_data = json.load(open(FILE_PATH_MATERIAL_CERTIFICATE_V1_COMPLETE))
    return MaterialCertificateV1(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def material_certificate_v1_doc_empty() -> MaterialCertificateV1:
    json_data = json.load(open(FILE_PATH_MATERIAL_CERTIFICATE_V1_EMPTY))
    return MaterialCertificateV1(json_data["document"]["inference"], page_n=None)


def test_empty_doc_constructor(material_certificate_v1_doc_empty):
    assert material_certificate_v1_doc_empty.certificate_type.value is None
    assert material_certificate_v1_doc_empty.norm.value is None
    assert material_certificate_v1_doc_empty.heat_number.value is None


def test_doc_constructor(material_certificate_v1_doc):
    file_path = f"{ MATERIAL_CERTIFICATE_DATA_DIR }/response_v1/doc_to_string.rst"
    reference_str = open(file_path, "r", encoding="utf-8").read()
    assert str(material_certificate_v1_doc) == reference_str
